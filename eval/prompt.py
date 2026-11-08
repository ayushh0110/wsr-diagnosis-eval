"""Build the single-turn prompt for one case.

Only `user_report`, `environment`, the listed artifacts and the optional experiments log are sent.
`title`, `tier`, `answer.json` and `evidence/` never reach the model (tests/test_prompt.py checks this).
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .cases import Case

PROMPT_VERSION = "1"
MAX_ARTIFACT_CHARS = 20_000

SYSTEM = """You are an experienced LLM inference engineer. A user running a local or self-hosted language model reports a failure and shares the artifacts they collected.

Find the single root cause that best explains the observed failure, and prescribe the fix.

- Decide from the evidence in the artifacts, not from what is usually true.
- Pick exactly one cause code from the list you are given, and the verdict category that code belongs to.
- If the artifacts do not show enough to name a cause, use verdict "inconclusive" with cause INSUFFICIENT_EVIDENCE and the fix action "collect_more_evidence", naming the experiment.
- Reply with one JSON object only, no other text."""

# Ablations: one extra instruction appended to the system prompt. "base" is the prompt every reported score uses.
VARIANTS = {
    "base": "",
    "mechanism": "- Before blaming any setting, work out what it actually does in this specific runtime, given the other "
                 "settings, the runtime's defaults and the order in which it applies them.",
}


def prompt_version(variant: str = "base") -> str:
    return PROMPT_VERSION if variant == "base" else f"{PROMPT_VERSION}+{variant}"


ANSWER_SHAPE = """{
  "verdict": "<one verdict key>",
  "cause": "<one cause code>",
  "fix": {"action": "<one fix action>", "target": "<parameter / field / flag / experiment, or null>", "value": "<new value, or null>"},
  "rationale": "<the evidence that decided it, 2-4 sentences>"
}"""


def _artifact_block(case: Case, art: dict[str, Any]) -> str:
    text = (case.dir / art["path"]).read_text(encoding="utf-8", errors="replace")
    note = ""
    if len(text) > MAX_ARTIFACT_CHARS:
        text = text[:MAX_ARTIFACT_CHARS]
        note = f"\n[truncated by the eval harness at {MAX_ARTIFACT_CHARS} characters]"
    fence = "````" if "```" in text else "```"
    return f"### {art['name']} ({art['path']})\n{fence}{art.get('lang', '')}\n{text}\n{fence}{note}"


def _codes_block(codes: dict[str, Any]) -> str:
    verdicts = "\n".join(f"- {k}: {v}" for k, v in codes["verdicts"].items())
    causes = "\n".join(f"- {c['code']} ({c['category']}): {c['description']}" for c in codes["codes"])
    actions = "\n".join(f"- {k}: {v}" for k, v in codes["fix_actions"].items())
    return f"## Verdicts\n{verdicts}\n\n## Cause codes\n{causes}\n\n## Fix actions\n{actions}"


def build_messages(case: Case, codes: dict[str, Any], variant: str = "base") -> list[dict[str, str]]:
    system = SYSTEM + ("\n" + VARIANTS[variant] if VARIANTS[variant] else "")
    m = case.meta
    env = "\n".join(f"- {k}: {v}" for k, v in (m.get("environment") or {}).items())
    parts = [f"## User report\n{m['user_report']}"]
    if env:
        parts.append(f"## Environment\n{env}")
    parts.append("## Artifacts\n" + "\n\n".join(_artifact_block(case, a) for a in m.get("artifacts", [])))
    if m.get("experiments_log"):
        log = (case.dir / m["experiments_log"]).read_text(encoding="utf-8")
        parts.append(f"## What the user already tried\n{log}")
    parts.append(_codes_block(codes))
    parts.append(f"## Answer\nReturn only this JSON object:\n{ANSWER_SHAPE}")
    return [{"role": "system", "content": system}, {"role": "user", "content": "\n\n".join(parts)}]


def prompt_hash(messages: list[dict[str, str]]) -> str:
    return hashlib.sha256(json.dumps(messages, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
