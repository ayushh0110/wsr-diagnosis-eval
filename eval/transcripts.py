"""Readable transcripts: one Markdown file per case with the exact prompt, the key and every model's replies.

    python -m eval.transcripts results/2026-11-08        # -> results/2026-11-08/transcripts/<case>.md

The prompt is rebuilt with eval/prompt.py and checked against the sha256 stored in each raw record, so the file
shows exactly what the models saw. Grades come from the same grader as scores.csv.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from .cases import CASES_DIR, load_cases, load_codes
from .grade import parse_response, score_answer
from .prompt import build_messages, prompt_hash


def _fence(text: str, lang: str = "") -> str:
    fence = "````" if "```" in text else "```"
    return f"{fence}{lang}\n{text}\n{fence}"


def write_transcripts(run_dir: Path, cases_dir: Path = CASES_DIR) -> Path:
    codes = load_codes()
    cases = {c.id: c for c in load_cases(cases_dir)}
    recs: dict[str, list[dict]] = defaultdict(list)
    for f in sorted((run_dir / "raw").glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        recs[rec["case_id"]].append(rec)
    out_dir = run_dir / "transcripts"
    out_dir.mkdir(exist_ok=True)
    index = ["# Transcripts", "", "| case | tier | strict passes | file |", "|---|---|---|---|"]
    for cid in sorted(recs):
        case = cases[cid]
        variant = recs[cid][0].get("prompt_variant", "base")
        messages = build_messages(case, codes, variant)
        sha = prompt_hash(messages)
        stale = sorted({r["prompt_sha256"] for r in recs[cid] if r.get("prompt_sha256") != sha})
        k = case.key
        L = [f"# {cid}", "", f"Tier: {case.tier}. {case.meta.get('title', '')}", "",
             f"**Key:** verdict `{k['verdict']}`, cause `{k['primary_cause']}`, reference fix "
             f"`{json.dumps(k['golden_fix'], ensure_ascii=False)}`.",
             f"Distractors: {', '.join(f'`{d}`' for d in k.get('distractors', {}))}.", "",
             f"Evidence for the key: `{case.dir.relative_to(case.dir.parent.parent).as_posix()}/answer.json` "
             f"(provenance) and `evidence/`.", ""]
        if stale:
            L += [f"> Note: {len(stale)} prompt hash(es) in the raw records differ from today's prompt.", ""]
        L += ["## Prompt (identical for every model and trial)", "",
              f"sha256 prefix `{sha}`" + (f", prompt variant `{variant}`" if variant != "base" else ""), "",
              "### System", "", _fence(messages[0]["content"]), "", "### User", "", _fence(messages[1]["content"]), "",
              "## Replies", ""]
        passed = 0
        for rec in sorted(recs[cid], key=lambda r: (r["model"], r["run"])):
            s = score_answer(parse_response(rec.get("final_content")), k, codes)
            passed += bool(s["strict"])
            mark = "PASS" if s["strict"] else ("decoy" if s.get("distractor_hit") else "fail")
            L += [f"### {rec['model']}, trial {rec['run']}: {mark} (score {s['score']:.2f}; "
                  f"verdict {'ok' if s['verdict_ok'] else 'wrong'}, cause {'ok' if s['cause_ok'] else 'wrong'}, "
                  f"fix {'ok' if s['fix_ok'] else 'wrong'})", "",
                  _fence(rec.get("final_content") or "(no reply)", "json"), ""]
            if len(rec.get("attempts", [])) > 1:
                L += [f"_{len(rec['attempts'])} attempts: the first reply did not parse; the final reply above is from "
                      "the format retry._", ""]
        name = f"{cid}.md"
        (out_dir / name).write_text("\n".join(L), encoding="utf-8")
        index.append(f"| {cid} | {case.tier} | {passed}/{len(recs[cid])} | [{name}]({name}) |")
    (out_dir / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return out_dir


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--cases", type=Path, default=CASES_DIR)
    args = ap.parse_args(argv)
    print(f"wrote {write_transcripts(args.run_dir, args.cases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
