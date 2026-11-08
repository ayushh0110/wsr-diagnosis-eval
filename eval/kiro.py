"""Second backend: models reached through the Kiro CLI with a Kiro API key (`kiro/<model>` ids in models.txt).

Kiro API keys (`ksk_...`) are documented only for `kiro-cli chat --no-interactive`
(https://kiro.dev/docs/getting-started/authentication/); there is no documented HTTP endpoint. So this backend
runs the CLI once per call with a workspace agent that has **no tools** and our system prompt, and passes the user
message as the prompt. Kiro adds its own harness around the model (its base instructions are not visible to us),
and temperature / max_tokens cannot be set; the run records this. Needs `kiro-cli` on PATH and KIRO_API_KEY.
"""
from __future__ import annotations

import atexit
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

PREFIX = "kiro/"
_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
_CREDITS = re.compile(r"Credits:\s*([0-9.]+)")
_AGENT_DIRS: dict[str, Path] = {}
_AGENT_LOCK = threading.Lock()  # workers call _agent_dir concurrently


def is_kiro(model_id: str) -> bool:
    return model_id.startswith(PREFIX)


def _agent_dir(system: str) -> Path:
    """A temp workspace holding .kiro/agents/diag.json: our system prompt, no tools, no MCP."""
    with _AGENT_LOCK:
        return _AGENT_DIRS.get(system) or _make_agent_dir(system)


def _make_agent_dir(system: str) -> Path:
    d = Path(tempfile.mkdtemp(prefix="wsr-eval-kiro-"))
    atexit.register(shutil.rmtree, d, ignore_errors=True)
    agent = {"name": "diag", "description": "single-turn diagnosis, no tools", "prompt": system,
             "tools": [], "allowedTools": [], "resources": [], "includeMcpJson": False, "mcpServers": {}}
    (d / ".kiro" / "agents").mkdir(parents=True)
    (d / ".kiro" / "agents" / "diag.json").write_text(json.dumps(agent, indent=2), encoding="utf-8")
    _AGENT_DIRS[system] = d
    return d


def _flatten(messages: list[dict[str, str]]) -> tuple[str, str]:
    """System prompt, and the conversation after it as one prompt (only the format retry has more than one turn)."""
    system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
    rest = [m for m in messages if m["role"] != "system"]
    if len(rest) == 1:
        return system, rest[0]["content"]
    parts = []
    for m in rest:
        parts.append(m["content"] if m["role"] == "user" else f"[Your previous reply]\n{m['content']}")
    return system, "\n\n".join(parts)


def clean(stdout: str) -> str:
    t = _ANSI.sub("", stdout).strip()
    return t[1:].lstrip() if t.startswith(">") else t


def call_kiro(model: dict[str, Any], messages: list[dict[str, str]], timeout: float = 900, tries: int = 3) -> dict:
    exe = shutil.which("kiro-cli")
    name = model["id"][len(PREFIX):]
    req = {"backend": "kiro-cli chat --no-interactive", "model": name, "agent": "diag (no tools)",
           "temperature": "not settable (Kiro default)", "max_tokens": "not settable"}
    if not exe:
        return {"request": req, "response": None, "error": "kiro-cli not found on PATH"}
    if not os.environ.get("KIRO_API_KEY"):
        return {"request": req, "response": None, "error": "KIRO_API_KEY is not set"}
    system, prompt = _flatten(messages)
    cwd = _agent_dir(system)
    try:
        version = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception:  # not fatal
        version = None
    req["kiro_cli"] = version
    last = None
    for i in range(tries):
        t0 = time.time()
        try:
            p = subprocess.run([exe, "chat", "--no-interactive", "--agent", "diag", "--model", name,
                                "--trust-tools=", prompt], cwd=cwd, capture_output=True, timeout=timeout,
                               encoding="utf-8", errors="replace", env={**os.environ, "NO_COLOR": "1"})
        except subprocess.TimeoutExpired:
            last = f"timeout after {timeout}s"
            continue
        out, err = clean(p.stdout or ""), _ANSI.sub("", p.stderr or "")
        credits = _CREDITS.search(err)
        if p.returncode == 0 and out:
            return {"request": req, "latency_s": round(time.time() - t0, 2),
                    "response": {"model": f"kiro/{name}", "choices": [{"message": {"content": out}}],
                                 "kiro_credits": float(credits.group(1)) if credits else None},
                    "stderr_tail": err.strip()[-400:]}
        last = f"exit {p.returncode}: {err.strip()[-600:]}"
        time.sleep(10 * (i + 1))
    return {"request": req, "response": None, "error": last}
