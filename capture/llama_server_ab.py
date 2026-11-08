"""One-factor A/B against a running OpenAI-compatible server (llama-server, Ollama /v1, vLLM).

The first arm is the failing request exactly as a user would send it. Each --variant changes
only the keys it names (null removes a key). Every arm runs --repeats times, so a flip counts only
if it reproduces.

Writes into the case folder:
  request.json, response.json   the failing arm, run 1 (shown to the model under test)
  server_cmd.txt                 the launch command you pass with --server-cmd (shown)
  evidence/                      every run of every arm, server /props, summary.md (never shown)

Example (case 04):
  python capture/llama_server_ab.py --case-dir cases/04_penalty_script_swap \
    --server-cmd "llama-server -m gemma-4-E2B-it-Q4_0.gguf --jinja -ngl 99 -c 4096" \
    --prompt "Explain how a refrigerator keeps food cold." \
    --params '{"temperature": 0, "max_tokens": 400, "repeat_penalty": 2.0,
               "chat_template_kwargs": {"enable_thinking": false}}' \
    --variant 'penalty_off={"repeat_penalty": null}' --repeats 2
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import detect, draft_case_json, env_info, load_json_arg, write_json, write_summary, write_text  # noqa: E402

PENALTY_KEYS = ("repeat_penalty", "repetition_penalty", "frequency_penalty", "presence_penalty")


def http(method: str, url: str, body: Optional[dict] = None, timeout: float = 600) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", errors="replace")
            status = r.status
    except urllib.error.HTTPError as e:
        raw, status = e.read().decode("utf-8", errors="replace"), e.code
    try:
        return status, json.loads(raw)
    except ValueError:
        return status, raw


def apply_variant(base: dict, change: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in change.items():
        if v is None:
            out.pop(k, None)
        else:
            out[k] = v
    return out


def is_penalised(params: dict) -> bool:
    for k in PENALTY_KEYS:
        v = params.get(k)
        if isinstance(v, (int, float)) and ((k.startswith("rep") and v > 1.15) or (not k.startswith("rep") and v > 0.5)):
            return True
    return False


def content_of(resp: Any) -> tuple[Optional[str], Optional[str]]:
    try:
        ch = resp["choices"][0]
        return ch["message"].get("content"), ch.get("finish_reason")
    except (TypeError, KeyError, IndexError):
        return None, None


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--case-dir", type=Path, required=True)
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--model", default="local", help="the 'model' field sent in the request")
    ap.add_argument("--server-cmd", required=True, help="the exact command the server was started with")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt", help="user message")
    g.add_argument("--messages", help="full messages list as JSON (or @file.json)")
    ap.add_argument("--system", help="system message, if the user sends one")
    ap.add_argument("--params", default="{}", help="request parameters of the failing arm: JSON or @file.json")
    ap.add_argument("--variant", action="append", default=[], metavar="NAME=JSON",
                    help="one-factor change: NAME=JSON or NAME=@file.json (repeatable)")
    ap.add_argument("--repeats", type=int, default=2)
    ap.add_argument("--expect-lang", help="language the reply should be in (for the detectors)")
    ap.add_argument("--no-artifacts", action="store_true", help="evidence only, do not write request/response.json")
    args = ap.parse_args(argv)

    if args.messages:
        msgs = load_json_arg(args.messages)
    else:
        msgs = ([{"role": "system", "content": args.system}] if args.system else []) + \
            [{"role": "user", "content": args.prompt}]
    base = {"model": args.model, "messages": msgs, **load_json_arg(args.params)}
    arms = [("failing", base)]
    for spec in args.variant:
        name, _, js = spec.partition("=")
        arms.append((name.strip(), apply_variant(base, load_json_arg(js))))

    case, ev = args.case_dir, args.case_dir / "evidence"
    root = args.base_url.rstrip("/")
    _, props = http("GET", root + "/props", timeout=30)
    _, models = http("GET", root + "/v1/models", timeout=30)
    write_json(ev / "server_props.json", {"props": props, "models": models})
    build = props.get("build_info") if isinstance(props, dict) else None

    user_text = next((m["content"] for m in reversed(msgs) if m["role"] == "user"
                      and isinstance(m["content"], str)), None)
    rows, first_resp = [], None
    for name, body in arms:
        for k in range(1, args.repeats + 1):
            t0 = time.time()
            status, resp = http("POST", root + "/v1/chat/completions", body)
            text, finish = content_of(resp)
            codes = detect(text or "", expect_lang=args.expect_lang, request=user_text,
                           penalised=is_penalised(body), finish_reason=finish) if text is not None else ["NO_CONTENT"]
            write_json(ev / f"{name}_r{k}.json", {"arm": name, "run": k, "request": body, "http_status": status,
                                                  "response": resp, "latency_s": round(time.time() - t0, 2),
                                                  "detector_codes": codes})
            settings = {kk: vv for kk, vv in body.items() if kk not in ("model", "messages")}
            rows.append({"arm": name, "run": k, "settings": settings, "codes": codes, "text": text, "finish": finish})
            print(f"{name} r{k}: HTTP {status}, finish={finish}, codes={codes}")
            if name == "failing" and k == 1:
                first_resp = resp

    write_json(ev / "env.json", env_info({"script": "llama_server_ab.py", "base_url": args.base_url,
                                          "server_build": build, "repeats": args.repeats,
                                          "arms": [a for a, _ in arms]}))
    summary = write_summary(case, rows, f"Server: `{args.server_cmd}` (build {build}). "
                                        f"Arms: {', '.join(a for a, _ in arms)}; {args.repeats} runs each.")

    if not args.no_artifacts:
        write_json(case / "request.json", base)
        write_json(case / "response.json", first_resp)
        write_text(case / "server_cmd.txt", args.server_cmd.strip() + "\n")
        draft_case_json(case, [
            {"name": "Request sent", "path": "request.json", "lang": "json"},
            {"name": "Raw response", "path": "response.json", "lang": "json"},
            {"name": "Server launch command", "path": "server_cmd.txt", "lang": "bash"},
        ], {"runtime": f"llama-server {build}" if build else "OpenAI-compatible server", "model": "<fill in: model file>",
            "precision": "<fill in: e.g. Q4_0>", "hardware": "<fill in>"})
    print(f"\nsummary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
