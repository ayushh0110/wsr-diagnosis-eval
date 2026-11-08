"""Shared helpers for the capture scripts: saving, scrubbing local details, failure detection, provenance."""
from __future__ import annotations

import datetime as dt
import getpass
import json
import os
import platform
import re
import socket
import sys
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------- scrubbing local details

_HOME = os.path.expanduser("~")
_USER = getpass.getuser()
_HOST = socket.gethostname()


def _scrub_str(s: str) -> str:
    for home in {_HOME, _HOME.replace("\\", "/"), _HOME.replace("\\", "\\\\")}:
        if home and len(home) > 3:
            s = s.replace(home, "~")
    if _USER and len(_USER) > 2:
        s = re.sub(rf"(?<=[\\/]){re.escape(_USER)}(?=[\\/])", "<user>", s)
    if _HOST and len(_HOST) > 2:
        s = s.replace(_HOST, "<host>")
    return s


def scrub(obj: Any) -> Any:
    """Remove home folder, user name and host name from every string inside obj."""
    if isinstance(obj, str):
        return _scrub_str(obj)
    if isinstance(obj, list):
        return [scrub(x) for x in obj]
    if isinstance(obj, tuple):
        return [scrub(x) for x in obj]
    if isinstance(obj, dict):
        return {scrub(k) if isinstance(k, str) else k: scrub(v) for k, v in obj.items()}
    return obj


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scrub(obj), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(scrub(text), encoding="utf-8")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- failure detection (wsr, optional)

def detect(text: str, *, expect_lang: Optional[str] = None, request: Optional[str] = None,
           penalised: bool = False, finish_reason: Optional[str] = None) -> Optional[list[str]]:
    """wsr's output detectors on one reply: the failing codes, or None when wsr is not installed.

    Used only to record what each run looked like. The answer key is decided by the flip itself
    (and your own reading of the replies), never by wsr's verdict.
    """
    try:
        from wsr.output import check_output  # type: ignore
    except Exception:
        return None
    fs = check_output(text or "", expect_lang=expect_lang, request=request, penalised=penalised,
                      finish_reason=finish_reason)
    return sorted({f.code for f in fs if f.failed} - {"TRUNCATED"})


def env_info(extra: Optional[dict] = None) -> dict[str, Any]:
    info: dict[str, Any] = {"captured_utc": now(), "python": sys.version.split()[0], "os": platform.platform()}
    try:
        import wsr  # type: ignore
        info["wsr"] = getattr(wsr, "__version__", "installed")
    except Exception:
        info["wsr"] = None
    if extra:
        info.update(extra)
    return info


# ---------------------------------------------------------------- case scaffolding

def draft_case_json(case_dir: Path, artifacts: list[dict[str, str]], environment: dict[str, str]) -> None:
    """Write case.json with the artifact list filled in, only if there is none yet (never overwrite your edits)."""
    p = case_dir / "case.json"
    if p.exists():
        print(f"kept existing {p.name}; artifacts written: {', '.join(a['path'] for a in artifacts)}")
        return
    write_json(p, {
        "id": case_dir.name,
        "title": "<fill in: one line for the report>",
        "tier": "<fill in: one tier from schema/CASE_FORMAT.md>",
        "user_report": "<fill in: the complaint in the user's words, no cause names>",
        "environment": environment,
        "artifacts": artifacts,
        "experiments_log": None,
    })
    print(f"drafted {p} (fill in the <fill in: ...> fields)")


def write_summary(case_dir: Path, rows: list[dict[str, Any]], header: str) -> Path:
    """evidence/summary.md: one line per run, and whether each variant flipped the failure."""
    L = [f"# Capture summary: {case_dir.name}", "", header, "",
         "| arm | run | settings | failure codes (wsr) | finish | first 120 chars |", "|---|---|---|---|---|---|"]
    for r in rows:
        codes = "n/a (wsr not installed)" if r["codes"] is None else (", ".join(r["codes"]) or "none")
        snippet = (r["text"] or "").replace("\n", " \\n ").replace("|", "\\|")[:120]
        L.append(f"| {r['arm']} | {r['run']} | `{json.dumps(r['settings'], ensure_ascii=False)}` | {codes} | "
                 f"{r.get('finish')} | {snippet} |")
    L += ["", "## Flip check", ""]
    arms = list(dict.fromkeys(r["arm"] for r in rows))
    first = arms[0]

    def failed(r: dict) -> Optional[bool]:
        return None if r["codes"] is None else bool(r["codes"])

    base = [failed(r) for r in rows if r["arm"] == first]
    for a in arms[1:]:
        other = [failed(r) for r in rows if r["arm"] == a]
        if None in base or None in other:
            L.append(f"- {a}: wsr not installed, read the replies above and decide yourself")
        elif all(base) and not any(other):
            L.append(f"- {a}: **flip reproduced** ({first} failed {len(base)}/{len(base)}, {a} passed "
                     f"{len(other)}/{len(other)})")
        elif all(base) and all(other):
            L.append(f"- {a}: **no flip**: the failure persists under this change ({len(other)}/{len(other)})")
        else:
            L.append(f"- {a}: mixed ({first}: {sum(base)}/{len(base)} failed, {a}: {sum(other)}/{len(other)} "
                     "failed). Not usable as a clean flip; read the replies")
    L += ["", "Detector codes are a record, not the answer key. Read every reply before writing answer.json."]
    p = case_dir / "evidence" / "summary.md"
    write_text(p, "\n".join(L) + "\n")
    return p


def parse_kv(spec: str) -> dict[str, Any]:
    """'a=1,b=true,c=null,d=text' -> {'a': 1, 'b': True, 'c': None, 'd': 'text'} (values parsed as JSON when they can be)."""
    out: dict[str, Any] = {}
    if not spec:
        return out
    for part in re.split(r",(?=[A-Za-z_][\w.]*=)", spec):
        if not part.strip():
            continue
        k, _, v = part.partition("=")
        try:
            out[k.strip()] = json.loads(v)
        except ValueError:
            out[k.strip()] = v
    return out


def load_json_arg(v: str) -> Any:
    """A JSON argument given inline, or as @path to a file (PowerShell-friendly)."""
    v = v.strip()
    if v.startswith("@"):
        return json.loads(Path(v[1:]).read_text(encoding="utf-8-sig"))
    return json.loads(v)
