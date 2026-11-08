"""Send every case to every model and save the raw outputs. Then grade.

    python -m eval.run --models models.txt              # real run (keys in env or .env)
    python -m eval.run --mock                           # no key: oracle + naive mock models, checks the pipeline
    python -m eval.run --models models.txt --only 04_penalty_script_swap --runs 1   # pilot

Models file: one id per line; lines starting with # are skipped.
  provider/model [| temperature=0 | temperature=default]   OpenRouter (OPENROUTER_API_KEY); `default` sends none
  gemini/<model> [| temperature=...]                        Google AI Studio, OpenAI-compatible (GEMINI_API_KEY)
  kiro/<model>                                              Kiro CLI (KIRO_API_KEY, kiro-cli on PATH; see kiro.py)

Outputs: results/<run_name>/raw/<case>__<model>__r<k>.json, run_meta.json, scores.csv, summary.md.
Existing raw files are kept, so an interrupted run resumes where it stopped; a stored reply that never got its
format retry gets it on resume. run_meta.json keeps the first start time and records every later invocation.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Optional

from .cases import CASES_DIR, ROOT, Case, load_cases, load_codes
from .grade import parse_response
from .kiro import call_kiro, is_kiro
from .prompt import VARIANTS, build_messages, prompt_hash, prompt_version

API_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1") + "/chat/completions"
# Other OpenAI-compatible providers, chosen by model-id prefix: prefix -> (chat completions URL, key variable)
PROVIDERS = {
    "gemini/": ("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "GEMINI_API_KEY"),
}
RETRY_MSG = "Your reply was not a single valid JSON object. Return only the JSON object, nothing else."
MOCKS = {"mock/oracle", "mock/naive-finetune"}


def provider(model_id: str) -> tuple[str, str, str]:
    """(url, key variable, model name to send) for a model id."""
    for prefix, (url, key_var) in PROVIDERS.items():
        if model_id.startswith(prefix):
            return url, key_var, model_id[len(prefix):]
    return API_URL, "OPENROUTER_API_KEY", model_id


def endpoint(model_id: str) -> str:
    if model_id in MOCKS:
        return "mock"
    return "kiro-cli chat --no-interactive" if is_kiro(model_id) else provider(model_id)[0]


def load_env(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_models(path: Path, default_temp: Optional[float]) -> list[dict[str, Any]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        mid, _, opts = (p.strip() for p in line.partition("|"))
        temp: Optional[float] = default_temp
        m = re.search(r"temperature\s*=\s*(\S+)", opts)
        if m:
            temp = None if m.group(1) == "default" else float(m.group(1))
        if is_kiro(mid):
            temp = None  # Kiro CLI cannot set temperature; nothing is sent, the provider default applies
        out.append({"id": mid, "temperature": temp})
    return out


# ---------------------------------------------------------------- model calls

def _post(url: str, body: dict[str, Any], key: str, timeout: float) -> dict[str, Any]:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "X-Title": "wsr-diagnosis-eval"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def call_model(model: dict[str, Any], messages: list[dict], max_tokens: int,
               timeout: float = 600, tries: int = 5) -> dict[str, Any]:
    if is_kiro(model["id"]):
        return call_kiro(model, messages)
    url, key_var, name = provider(model["id"])
    key = os.environ.get(key_var, "")
    body: dict[str, Any] = {"model": name, "messages": messages, "max_tokens": max_tokens}
    if model["temperature"] is not None:
        body["temperature"] = model["temperature"]
    request_record = {"endpoint": url, **{k: v for k, v in body.items() if k != "messages"}}
    last: Any = None
    for i in range(tries):
        t0 = time.time()
        try:
            resp = _post(url, body, key, timeout)
            if "error" in resp and not resp.get("choices"):
                raise RuntimeError(json.dumps(resp["error"])[:500])
            return {"request": request_record, "response": resp, "latency_s": round(time.time() - t0, 2)}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}"
            if e.code not in (408, 409, 429, 500, 502, 503, 504):
                break
        except (urllib.error.URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as e:
            last = repr(e)
        time.sleep(min(60, 5 * 2 ** i))
    return {"request": request_record, "response": None, "error": last}


def mock_answer(model_id: str, case: Case) -> str:
    if model_id == "mock/oracle":
        k = case.key or {}
        return json.dumps({"verdict": k.get("verdict"), "cause": k.get("primary_cause"),
                           "fix": k.get("golden_fix"), "rationale": "oracle: copies the answer key"})
    return json.dumps({"verdict": "weight_level", "cause": "WEIGHT_OTHER",
                       "fix": {"action": "weight_edit_or_finetune", "target": "model", "value": None},
                       "rationale": "naive baseline: always blames the model"})


def _content(resp: Optional[dict]) -> Optional[str]:
    try:
        return resp["choices"][0]["message"]["content"]
    except (TypeError, KeyError, IndexError):
        return None


def format_retry(rec: dict[str, Any], messages: list[dict], model: dict[str, Any], max_tokens: int,
                 note: Optional[str] = None) -> None:
    """The one retry a reply gets when it holds no answer object: ask again for JSON only, keep the better reply."""
    retry = messages + [{"role": "assistant", "content": rec["final_content"] or ""},
                        {"role": "user", "content": RETRY_MSG}]
    att = call_model(model, retry, max_tokens)
    rec["attempts"].append({**att, "note": note} if note else att)
    if parse_response(_content(att.get("response"))) is not None:
        rec["final_content"] = _content(att.get("response"))


def run_one(case: Case, model: dict[str, Any], run: int, codes: dict, max_tokens: int,
            variant: str = "base") -> dict:
    messages = build_messages(case, codes, variant)
    rec: dict[str, Any] = {"case_id": case.id, "model": model["id"], "run": run,
                           "prompt_version": prompt_version(variant), "prompt_variant": variant,
                           "prompt_sha256": prompt_hash(messages),
                           "settings": {"temperature": model["temperature"],
                                        "max_tokens": None if is_kiro(model["id"]) else max_tokens},
                           "started": dt.datetime.now(dt.timezone.utc).isoformat(), "attempts": []}
    if model["id"] in MOCKS:
        rec["model_returned"] = model["id"]
        rec["final_content"] = mock_answer(model["id"], case)
        rec["attempts"].append({"mock": True})
        return rec
    att = call_model(model, messages, max_tokens)
    rec["attempts"].append(att)
    rec["final_content"] = _content(att.get("response"))
    if att.get("response") is not None and rec["final_content"] is None:
        rec["final_content"] = ""  # the provider answered with no text: grade it (format failure), don't retry it
    if att.get("response") is not None and parse_response(rec["final_content"]) is None:
        format_retry(rec, messages, model, max_tokens)
    rec["model_returned"] = (att.get("response") or {}).get("model")
    rec["finished"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return rec


def write_run_meta(path: Path, models: list[dict], cases: list[Case], args: argparse.Namespace) -> None:
    """Create run_meta.json, or merge into it on resume: first start time kept, cases unioned, invocations listed."""
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    meta = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"date_utc": now}
    merged = {m["id"]: m for m in meta.get("models", [])} | {m["id"]: m for m in models}
    meta.pop("endpoint", None)
    meta.update({"models": list(merged.values()), "runs": args.runs, "max_tokens": args.max_tokens,
                 "prompt_version": prompt_version(args.prompt_variant),
                 "cases": sorted(set(meta.get("cases", [])) | {c.id for c in cases}),
                 "endpoints": {mid: endpoint(mid) for mid in merged}})
    meta.setdefault("invocations", []).append({"started_utc": now, "cases": [c.id for c in cases]})
    path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", type=Path, help="file with model ids (see models.example.txt)")
    ap.add_argument("--mock", action="store_true", help="use the two mock models, no API key needed")
    ap.add_argument("--cases", type=Path, default=CASES_DIR)
    ap.add_argument("--only", nargs="*", help="case ids or folder names")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--temperature", default="0", help="default temperature, or 'default' to send none")
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--prompt-variant", choices=sorted(VARIANTS), default="base",
                    help="ablation: append one instruction to the system prompt (see eval/prompt.py)")
    ap.add_argument("--name", help="results/<name>; default: today's date (UTC)")
    ap.add_argument("--results", type=Path, default=ROOT / "results", help="parent folder for run folders")
    args = ap.parse_args(argv)

    load_env()
    default_temp = None if args.temperature == "default" else float(args.temperature)
    if args.mock:
        models = [{"id": m, "temperature": None} for m in sorted(MOCKS)]
    else:
        if not args.models:
            ap.error("--models is required (or --mock)")
        models = parse_models(args.models, default_temp)
        needed = sorted({"KIRO_API_KEY" if is_kiro(m["id"]) else provider(m["id"])[1] for m in models})
        missing = [v for v in needed if not os.environ.get(v)]
        if missing:
            print(f"not set (environment or .env): {', '.join(missing)}", file=sys.stderr)
            return 2

    codes = load_codes()
    cases = [c for c in load_cases(args.cases, args.only) if c.key is not None or not args.mock]
    if not cases:
        print("no cases found", file=sys.stderr)
        return 2
    name = args.name or ("mock-" if args.mock else "") + dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    run_dir = args.results / name
    (run_dir / "raw").mkdir(parents=True, exist_ok=True)
    meta_path = run_dir / "run_meta.json"
    if meta_path.exists():
        old = json.loads(meta_path.read_text(encoding="utf-8")).get("prompt_version")
        if old and old != prompt_version(args.prompt_variant):
            print(f"{run_dir} holds prompt version {old}; use another --name for this variant", file=sys.stderr)
            return 2
    write_run_meta(meta_path, models, cases, args)

    jobs, retries = [], []
    for c in cases:
        for m in models:
            for k in range(1, args.runs + 1):
                out = run_dir / "raw" / f"{c.id}__{_slug(m['id'])}__r{k}.json"
                prev = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
                if prev.get("final_content") is None:
                    jobs.append((c, m, k, out))
                elif (parse_response(prev["final_content"]) is None and len(prev.get("attempts", [])) == 1
                      and m["id"] not in MOCKS):
                    retries.append((c, m, k, out, prev))
    print(f"{len(jobs)} calls to make ({len(cases)} cases x {len(models)} models x {args.runs} runs, minus done)")

    for c, m, k, out, prev in retries:
        format_retry(prev, build_messages(c, codes, args.prompt_variant), m, args.max_tokens,
                     note="format retry applied on resume")
        out.write_text(json.dumps(prev, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"retry {c.id} {m['id']} r{k}: {'parsed' if parse_response(prev['final_content']) else 'still unparseable'}")

    failed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(run_one, c, m, k, codes, args.max_tokens, args.prompt_variant): (c, m, k, out)
                for c, m, k, out in jobs}
        for f in as_completed(futs):
            c, m, k, out = futs[f]
            try:
                rec = f.result()
            except Exception as e:  # keep the run going; the record says what happened
                rec = {"case_id": c.id, "model": m["id"], "run": k, "final_content": None, "attempts": [],
                       "error": repr(e)}
            out.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
            ok = rec.get("final_content") is not None
            failed += not ok
            print(f"{'ok ' if ok else 'ERR'} {c.id} {m['id']} r{k}")

    from .grade import main as grade_main
    grade_main([str(run_dir), "--cases", str(args.cases)])
    if failed:
        print(f"{failed} call(s) returned nothing; rerun the same command to retry them", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
