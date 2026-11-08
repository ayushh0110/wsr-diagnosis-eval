"""Deterministic grader. No model calls; works offline on results/<run>/raw.

Per answer (0-1):
    0.4  verdict in acceptable_verdicts
    0.4  cause in acceptable_causes
    0.2  fix matches any acceptable_fixes entry (action, target regex, value range / pattern)
strict = all three right.

Flags (counted, not scored):
    overreach   truth is not weight_level, answer says weight_level or prescribes a weight edit / fine-tune
    underreach  truth is weight_level, answer blames something else
    overclaim   truth is inconclusive, answer names a definite cause
    distractor_hit  the chosen cause is one of the tempting wrong causes the key lists (the decoy)
    inconsistent  the verdict is not the category of the chosen cause code
    invalid_code / invalid_verdict / invalid_action  value outside the closed lists
    format_failure  no JSON object could be parsed (score 0)

Usage:  python -m eval.grade results/<run>
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

from .cases import CASES_DIR, load_cases, load_codes

W_VERDICT, W_CAUSE, W_FIX = 0.4, 0.4, 0.2
WEIGHT_ACTIONS = {"weight_edit_or_finetune"}

# ---------------------------------------------------------------- parsing


def parse_response(text: Optional[str]) -> Optional[dict[str, Any]]:
    """The answer object from a reply: whole text, a fenced block, or the first JSON object inside."""
    if not text:
        return None
    t = text.strip()
    try:
        v = json.loads(t)
        if isinstance(v, dict) and ("verdict" in v or "cause" in v):
            return v
    except ValueError:
        pass
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.S):
        try:
            v = json.loads(m.group(1))
            if isinstance(v, dict) and ("verdict" in v or "cause" in v):
                return v
        except ValueError:
            continue
    dec = json.JSONDecoder()
    for i, ch in enumerate(t):
        if ch != "{":
            continue
        try:
            v, _ = dec.raw_decode(t[i:])
        except ValueError:
            continue
        if isinstance(v, dict) and ("verdict" in v or "cause" in v):
            return v
    # no object carrying a verdict or cause (e.g. invalid outer JSON with a valid inner "fix" object): unparseable
    return None


def _norm_code(s: Any) -> str:
    return re.sub(r"[\s\-]+", "_", str(s or "").strip()).upper()


def _norm_key(s: Any) -> str:
    return re.sub(r"[\s\-]+", "_", str(s or "").strip()).lower()


def normalise(ans: dict[str, Any]) -> dict[str, Any]:
    fix = ans.get("fix")
    if isinstance(fix, str):
        fix = {"action": fix}
    if not isinstance(fix, dict):
        fix = {}
    return {
        "verdict": _norm_key(ans.get("verdict")),
        "cause": _norm_code(ans.get("cause")),
        "fix": {"action": _norm_key(fix.get("action")), "target": fix.get("target"), "value": fix.get("value")},
        "rationale": ans.get("rationale"),
    }


# ---------------------------------------------------------------- matching

_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _value_ok(spec: Optional[dict[str, Any]], value: Any) -> bool:
    if not spec:
        return True
    if "pattern" in spec:
        return value is not None and re.search(spec["pattern"], str(value), re.I) is not None
    if isinstance(value, bool) or value is None:
        return False
    # Any number in range counts, so "from 1.5 to 1.0" passes a max of 1.15 while "1.5" alone does not.
    nums = [float(n) for n in _NUM.findall(str(value))]
    return any(("min" not in spec or x >= spec["min"]) and ("max" not in spec or x <= spec["max"]) for x in nums)


def fix_matches(fix: dict[str, Any], acceptable: list[dict[str, Any]]) -> bool:
    for spec in acceptable:
        if fix.get("action") != spec["action"]:
            continue
        pat = spec.get("target_pattern")
        if pat and not re.search(pat, str(fix.get("target") or ""), re.I):
            continue
        if not _value_ok(spec.get("value"), fix.get("value")):
            continue
        return True
    return False


def score_answer(raw: Optional[dict[str, Any]], key: dict[str, Any], codes: dict[str, Any]) -> dict[str, Any]:
    truth_weight = key["verdict"] == "weight_level"
    truth_inconclusive = key["verdict"] == "inconclusive"
    if raw is None:
        return {"parsed": False, "format_failure": True, "score": 0.0, "strict": False, "verdict_ok": False,
                "cause_ok": False, "fix_ok": False, "overreach": False, "underreach": truth_weight,
                "overclaim": False, "distractor_hit": False, "inconsistent": False, "invalid_code": False, "invalid_verdict": False,
                "invalid_action": False, "verdict": None, "cause": None, "fix_action": None}
    a = normalise(raw)
    by_code = codes["by_code"]
    verdict_ok = a["verdict"] in key["acceptable_verdicts"]
    cause_ok = a["cause"] in key["acceptable_causes"]
    fix_ok = fix_matches(a["fix"], key["acceptable_fixes"])
    weightish = a["verdict"] == "weight_level" or a["fix"]["action"] in WEIGHT_ACTIONS
    cat = by_code.get(a["cause"], {}).get("category")
    score = W_VERDICT * verdict_ok + W_CAUSE * cause_ok + W_FIX * fix_ok
    return {
        "parsed": True,
        "format_failure": False,
        "score": round(score, 4),
        "strict": verdict_ok and cause_ok and fix_ok,
        "verdict_ok": verdict_ok,
        "cause_ok": cause_ok,
        "fix_ok": fix_ok,
        "overreach": (not truth_weight) and weightish,
        "underreach": truth_weight and a["verdict"] != "weight_level",
        "overclaim": truth_inconclusive and a["verdict"] != "inconclusive",
        "distractor_hit": a["cause"] in key.get("distractors", {}),
        "inconsistent": cat is not None and cat != a["verdict"],
        "invalid_code": a["cause"] not in by_code,
        "invalid_verdict": a["verdict"] not in codes["verdicts"],
        "invalid_action": a["fix"]["action"] not in codes["fix_actions"],
        "verdict": a["verdict"],
        "cause": a["cause"],
        "fix_action": a["fix"]["action"],
    }


# ---------------------------------------------------------------- run grading

FIELDS = ["case_id", "tier", "model", "model_returned", "run", "score", "strict", "verdict_ok", "cause_ok", "fix_ok",
          "verdict", "cause", "fix_action", "overreach", "underreach", "overclaim", "distractor_hit", "inconsistent", "invalid_code",
          "invalid_verdict", "invalid_action", "format_failure", "attempts"]


def grade_run(run_dir: Path, cases_dir: Path = CASES_DIR) -> list[dict[str, Any]]:
    codes = load_codes()
    cases = {c.id: c for c in load_cases(cases_dir)}
    rows = []
    for f in sorted((run_dir / "raw").glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        case = cases.get(rec["case_id"])
        if case is None or case.key is None:
            print(f"skip {f.name}: no case / answer key for {rec['case_id']}", file=sys.stderr)
            continue
        if rec.get("final_content") is None:  # the API never returned a reply (quota, outage): not a model answer
            print(f"skip {f.name}: no model reply (API error); rerun the same eval.run command to retry it",
                  file=sys.stderr)
            continue
        s = score_answer(parse_response(rec.get("final_content")), case.key, codes)
        rows.append({"case_id": case.id, "tier": case.tier, "model": rec["model"],
                     "model_returned": rec.get("model_returned"), "run": rec["run"],
                     "attempts": len(rec.get("attempts", [])), **{k: s[k] for k in FIELDS if k in s}})
    return rows


def write_scores(rows: list[dict[str, Any]], run_dir: Path) -> Path:
    out = run_dir / "scores.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in FIELDS})
    return out


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--cases", type=Path, default=CASES_DIR)
    args = ap.parse_args(argv)
    rows = grade_run(args.run_dir, args.cases)
    if not rows:
        print("no gradable outputs found", file=sys.stderr)
        return 1
    p = write_scores(rows, args.run_dir)
    from .report import write_report
    md = write_report(rows, args.run_dir)
    print(f"wrote {p} and {md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
