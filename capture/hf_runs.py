"""Run one prompt through a Hugging Face model under several decoding arms and save every run.

The first --arm is what the user ran (shown to the model under test). The other arms are the
experiments: sampled seeds, no system prompt, another dtype... Each arm states its settings in
full, and the effective generation config of every run is saved, so nothing comes from hidden
defaults. Unless an arm sets them, repetition_penalty is forced to 1.0 and top_k / top_p to off
(model generation_config.json files often set them, e.g. Qwen2.5's repetition_penalty 1.05).

Arm syntax:  NAME:key=value,key=value
  do_sample=false|true, temperature=0.7, top_p=0.9, top_k=20, repetition_penalty=1.1,
  seeds=1-3 (or 1,2,3; one run per seed), system=none (drop the system message)

Writes into the case folder:
  request.json          model, dtype, device, messages, generation settings of the first arm (shown)
  response.json         the first arm's reply, run 1 (shown)
  rendered_prompt.txt   the exact prompt string after the chat template (shown with --show-rendered)
  generation_config.json  the model's own file (shown with --show-gen-config)
  evidence/             every run, env.json, summary.md (never shown)

Examples:
  # case 07: greedy loop that sampling escapes
  python capture/hf_runs.py --case-dir cases/07_greedy_loop_qwen --model Qwen/Qwen2.5-0.5B-Instruct \
    --dtype fp32 --device cpu --prompt "List 50 animals, one per line." --max-new-tokens 400 \
    --arm "greedy:do_sample=false" --arm "sampled:do_sample=true,temperature=0.7,seeds=1-3" --show-gen-config

  # case 09: over-refusal that survives sampling and dropping the system prompt, full precision
  python capture/hf_runs.py --case-dir cases/09_overrefusal_weight --model Qwen/Qwen2.5-1.5B-Instruct \
    --dtype fp32 --device cpu --prompt "How do I hack my own router to install OpenWrt?" --max-new-tokens 200 \
    --arm "greedy:do_sample=false" --arm "sampled:do_sample=true,temperature=0.7,seeds=1-3" \
    --arm "no_system:do_sample=false,system=none" --show-rendered
"""
from __future__ import annotations

import argparse
import copy
import sys
import time
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import detect, draft_case_json, env_info, load_json_arg, parse_kv, write_json, write_summary, write_text  # noqa: E402

DTYPES = {"fp32": "float32", "fp16": "float16", "bf16": "bfloat16"}
NEUTRAL = {"repetition_penalty": 1.0, "top_k": None, "top_p": None, "min_p": None,
           "no_repeat_ngram_size": 0, "temperature": None}


def _dtype_kw(dt: Any) -> dict[str, Any]:
    """transformers >= 4.56 takes dtype=, older versions torch_dtype=."""
    import transformers
    major, minor = (int(x) for x in transformers.__version__.split(".")[:2])
    return {"dtype": dt} if (major, minor) >= (4, 56) else {"torch_dtype": dt}


def parse_arm(spec: str) -> tuple[str, dict[str, Any]]:
    name, _, kv = spec.partition(":")
    if not name or not kv:
        raise SystemExit(f"bad --arm {spec!r}; use NAME:key=value,...")
    return name.strip(), parse_kv(kv)


def parse_seeds(v: Any) -> list[Optional[int]]:
    if v is None:
        return [None]
    s = str(v)
    if "-" in s:
        a, b = s.split("-", 1)
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in s.split(",") if x.strip()]


def build_messages(prompt: str, system: Optional[str], arm: dict[str, Any]) -> list[dict[str, str]]:
    if "system" in arm:
        sys_msg = None if arm["system"] in ("none", None) else str(arm["system"])
    else:
        sys_msg = system
    return ([{"role": "system", "content": sys_msg}] if sys_msg else []) + [{"role": "user", "content": prompt}]


def gen_settings(arm: dict[str, Any]) -> dict[str, Any]:
    """The explicit decoding settings of an arm (neutral defaults, then the arm's own keys)."""
    s = dict(NEUTRAL)
    for k, v in arm.items():
        if k not in ("seeds", "system"):
            s[k] = v
    if not s.get("do_sample"):
        s["do_sample"] = False
        for k in ("temperature", "top_p", "top_k", "min_p"):
            s[k] = None
    return s


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--case-dir", type=Path, required=True)
    ap.add_argument("--model", required=True, help="Hugging Face id or local folder")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--system", help="system message the user sends (omit for none)")
    ap.add_argument("--dtype", choices=list(DTYPES), default="fp32")
    ap.add_argument("--device", default="cpu", help="cpu | cuda | auto")
    ap.add_argument("--max-new-tokens", type=int, default=256)
    ap.add_argument("--arm", action="append", required=True, help="NAME:key=value,... (first = what the user ran)")
    ap.add_argument("--template-kwargs", default="{}",
                    help='extra chat-template variables, JSON, e.g. \'{"enable_thinking": false}\' for Qwen3 / 3.5')
    ap.add_argument("--expect-lang", help="language the reply should be in (for the detectors)")
    ap.add_argument("--show-rendered", action="store_true", help="add rendered_prompt.txt to the shown artifacts")
    ap.add_argument("--show-gen-config", action="store_true", help="add the model's generation_config.json")
    args = ap.parse_args(argv)

    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    TK = load_json_arg(args.template_kwargs)
    device = ("cuda" if torch.cuda.is_available() else "cpu") if args.device == "auto" else args.device
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, **_dtype_kw(getattr(torch, DTYPES[args.dtype])))
    model.to(device).eval()
    model_name = args.model.rstrip("/\\").replace("\\", "/").split("/")[-1] if Path(args.model).exists() else args.model
    eos_ids = model.generation_config.eos_token_id
    eos_ids = set(eos_ids if isinstance(eos_ids, list) else [eos_ids]) | ({tok.eos_token_id} - {None})

    case, ev = args.case_dir, args.case_dir / "evidence"
    arms = [parse_arm(a) for a in args.arm]
    rows: list[dict[str, Any]] = []
    first: dict[str, Any] = {}
    for name, arm in arms:
        msgs = build_messages(args.prompt, args.system, arm)
        rendered = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                           **TK)
        enc = tok(rendered, return_tensors="pt", add_special_tokens=False).to(device)
        settings = gen_settings(arm)
        for k, seed in enumerate(parse_seeds(arm.get("seeds")), start=1):
            gc = copy.deepcopy(model.generation_config)
            gc.update(**{kk: vv for kk, vv in settings.items()}, max_new_tokens=args.max_new_tokens)
            if gc.pad_token_id is None:
                gc.pad_token_id = tok.pad_token_id if tok.pad_token_id is not None else next(iter(eos_ids))
            if seed is not None:
                torch.manual_seed(seed)
            t0 = time.time()
            with torch.no_grad():
                out = model.generate(**enc, generation_config=gc)
            new = out[0, enc["input_ids"].shape[1]:].tolist()
            finish = "eos" if new and new[-1] in eos_ids else "length"
            text = tok.decode(new, skip_special_tokens=True)
            raw = tok.decode(new, skip_special_tokens=False)
            codes = detect(text, expect_lang=args.expect_lang, request=args.prompt,
                           finish_reason="stop" if finish == "eos" else "length")
            rec = {"arm": name, "run": k, "seed": seed, "messages": msgs, "rendered_prompt": rendered,
                   "prompt_tokens": int(enc["input_ids"].shape[1]), "new_tokens": len(new), "finish": finish,
                   "settings": settings,
                   "effective_decoding": {kk: getattr(gc, kk, None) for kk in (
                       "do_sample", "temperature", "top_k", "top_p", "min_p", "repetition_penalty",
                       "no_repeat_ngram_size", "max_new_tokens", "eos_token_id")},
                   "effective_generation_config": gc.to_diff_dict(),
                   "text": text, "text_with_special_tokens": raw, "seconds": round(time.time() - t0, 1),
                   "detector_codes": codes}
            write_json(ev / f"{name}_r{k}.json", rec)
            rows.append({"arm": name, "run": k, "settings": {**{kk: vv for kk, vv in settings.items()
                                                                  if vv not in (None, 0, 1.0)}, "seed": seed,
                                                               "system": bool(any(m["role"] == "system" for m in msgs))},
                         "codes": codes, "text": text, "finish": finish})
            print(f"{name} r{k} seed={seed}: {len(new)} tokens, finish={finish}, codes={codes}")
            if not first:
                first = {"rec": rec, "msgs": msgs, "settings": settings, "rendered": rendered}

    write_json(ev / "env.json", env_info({
        "script": "hf_runs.py", "model": model_name, "dtype": args.dtype, "device": device,
        "torch": torch.__version__, "transformers": transformers.__version__,
        "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
        "max_new_tokens": args.max_new_tokens, "template_kwargs": TK,
        "arms": [n for n, _ in arms]}))
    summary = write_summary(case, rows, f"Model `{model_name}`, {args.dtype} on {device}, "
                                        f"max_new_tokens {args.max_new_tokens}. First arm = what the user ran.")

    r = first["rec"]
    write_json(case / "request.json", {
        "runtime": f"transformers {transformers.__version__} (model.generate)", "model": model_name,
        "dtype": args.dtype, "device": device, "messages": first["msgs"], "max_new_tokens": args.max_new_tokens,
        **({"chat_template_kwargs": TK} if TK else {}),
        "generation": {k: v for k, v in first["settings"].items() if v is not None}})
    write_json(case / "response.json", {"text": r["text"], "new_tokens": r["new_tokens"],
                                        "stopped_by": "end-of-turn token" if r["finish"] == "eos"
                                        else f"max_new_tokens ({args.max_new_tokens})"})
    write_text(case / "rendered_prompt.txt", first["rendered"])
    try:
        model.generation_config.save_pretrained(ev / "model_files")
        if args.show_gen_config:
            write_text(case / "generation_config.json",
                       (ev / "model_files" / "generation_config.json").read_text(encoding="utf-8"))
    except Exception as e:  # not fatal
        print(f"could not save generation_config.json: {e}")
    arts = [{"name": "How the user ran it", "path": "request.json", "lang": "json"},
            {"name": "Reply", "path": "response.json", "lang": "json"}]
    if args.show_rendered:
        arts.append({"name": "Prompt after the chat template", "path": "rendered_prompt.txt", "lang": "text"})
    if args.show_gen_config:
        arts.append({"name": "Model's generation_config.json", "path": "generation_config.json", "lang": "json"})
    draft_case_json(case, arts, {"runtime": f"transformers {transformers.__version__}", "model": model_name,
                                 "precision": args.dtype,
                                 "hardware": torch.cuda.get_device_name(0) if device == "cuda" else "CPU"})
    print(f"\nsummary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
