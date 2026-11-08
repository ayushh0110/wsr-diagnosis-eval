"""Markdown summary of graded rows: per model, per tier, per case, and the most common wrong answers."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

TIERS = ["control", "red_herring", "decoy_setting", "decoy_documented", "decoy_twin", "decoy_reverse", "dont_blame_weights",
         "blame_weights", "inconclusive"]


def _mean(xs: list[float]) -> str:
    return f"{sum(xs) / len(xs):.2f}" if xs else "-"


def _rate(rows: list[dict[str, Any]], flag: str, cond) -> str:
    sel = [r for r in rows if cond(r)]
    return f"{sum(bool(r[flag]) for r in sel)}/{len(sel)}" if sel else "-"


def pass_at_k(rows: list[dict[str, Any]]) -> tuple[int, float, float]:
    """(k, pass@k, pass^k) over cases: a case passes@k if any trial is strict, ^k if every trial is.
    k is the smallest number of trials any case has, and only the first k trials of each case count."""
    by_case: dict[str, list] = defaultdict(list)
    for r in sorted(rows, key=lambda r: int(r["run"])):
        by_case[r["case_id"]].append(bool(r["strict"]))
    k = min(len(v) for v in by_case.values())
    trials = [v[:k] for v in by_case.values()]
    return k, sum(any(t) for t in trials) / len(trials), sum(all(t) for t in trials) / len(trials)


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_model: dict[str, list] = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    out = {}
    for m, rs in sorted(by_model.items()):
        k, at_k, hat_k = pass_at_k(rs)
        out[m] = {
            "runs": len(rs),
            "mean_score": round(sum(r["score"] for r in rs) / len(rs), 4),
            "strict_pass": round(sum(bool(r["strict"]) for r in rs) / len(rs), 4),
            "k": k,
            "pass_at_k": round(at_k, 4),
            "pass_hat_k": round(hat_k, 4),
            "by_tier": {t: round(sum(r["score"] for r in rs if r["tier"] == t) /
                                 max(1, sum(1 for r in rs if r["tier"] == t)), 4)
                        for t in TIERS if any(r["tier"] == t for r in rs)},
            "overreach": sum(bool(r["overreach"]) for r in rs),
            "underreach": sum(bool(r["underreach"]) for r in rs),
            "overclaim": sum(bool(r["overclaim"]) for r in rs),
            "format_failures": sum(bool(r["format_failure"]) for r in rs),
            "distractor_hits": sum(bool(r.get("distractor_hit")) for r in rs),
            "models_returned": sorted({str(r.get("model_returned")) for r in rs}),
        }
    return out


def write_report(rows: list[dict[str, Any]], run_dir: Path) -> Path:
    summ = summarise(rows)
    (run_dir / "summary.json").write_text(json.dumps(summ, indent=2), encoding="utf-8")
    models = list(summ)
    tiers = [t for t in TIERS if any(r["tier"] == t for r in rows)]
    L = [f"# Results: {run_dir.name}", ""]

    L += ["## Per model", "",
          "| model | runs | mean | strict | " + " | ".join(tiers) +
          " | overreach | underreach | overclaim | took the decoy | format fail |",
          "|---|---|---|---|" + "---|" * len(tiers) + "---|---|---|---|---|"]
    for m in models:
        rs = [r for r in rows if r["model"] == m]
        s = summ[m]
        L.append(f"| {m} | {s['runs']} | {s['mean_score']:.2f} | {s['strict_pass']:.0%} | " +
                 " | ".join(_mean([r["score"] for r in rs if r["tier"] == t]) for t in tiers) + " | " +
                 _rate(rs, "overreach", lambda r: r["tier"] != "blame_weights") + " | " +
                 _rate(rs, "underreach", lambda r: r["tier"] == "blame_weights") + " | " +
                 _rate(rs, "overclaim", lambda r: r["tier"] == "inconclusive") + " | " +
                 f"{s['distractor_hits']}/{s['runs']} | {s['format_failures']} |")

    L += ["", "Overreach: blamed the weights (or prescribed a weight edit / fine-tune) on a non-weight case. "
          "Underreach: blamed a setting on a weight-level case. Overclaim: named a cause on an inconclusive case.", ""]

    L += ["## Consistency over trials", "",
          "Pass = strict (verdict, cause and fix all right). pass@k: the case was passed in at least one of k trials; "
          "pass^k: in all k.", "",
          "| model | cases | trials per case (k) | pass rate (per trial) | pass@k | pass^k |", "|---|---|---|---|---|---|"]
    for m in models:
        s = summ[m]
        n_cases = len({r["case_id"] for r in rows if r["model"] == m})
        L.append(f"| {m} | {n_cases} | {s['k']} | {s['strict_pass']:.0%} | {s['pass_at_k']:.0%} | {s['pass_hat_k']:.0%} |")
    L.append("")

    cases = sorted({(r["case_id"], r["tier"]) for r in rows})
    L += ["## Per case (strict passes / trials)", "", "| case | tier | " + " | ".join(models) + " |",
          "|---|---|" + "---|" * len(models)]
    for cid, tier in cases:
        cells = []
        for m in models:
            rs = [r for r in rows if r["case_id"] == cid and r["model"] == m]
            cells.append(f"{sum(bool(r['strict']) for r in rs)}/{len(rs)}" if rs else "-")
        L.append(f"| {cid} | {tier} | " + " | ".join(cells) + " |")
    L.append("")

    L += ["## Per case (mean score over runs)", "", "| case | tier | " + " | ".join(models) + " |",
          "|---|---|" + "---|" * len(models)]
    for cid, tier in cases:
        L.append(f"| {cid} | {tier} | " + " | ".join(
            _mean([r["score"] for r in rows if r["case_id"] == cid and r["model"] == m]) for m in models) + " |")

    L += ["", "## Most common wrong causes", "", "| case | wrong cause | count | models |", "|---|---|---|---|"]
    for cid, _ in cases:
        wrong = [r for r in rows if r["case_id"] == cid and not r["cause_ok"]]
        cnt = Counter(r["cause"] or "(no answer)" for r in wrong)
        for cause, n in cnt.most_common(3):
            ms = sorted({r["model"] for r in wrong if (r["cause"] or "(no answer)") == cause})
            L.append(f"| {cid} | {cause} | {n} | {', '.join(ms)} |")

    out = run_dir / "summary.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out
