"""Uncertainty for the headline numbers: Wilson 95% intervals on pass rates, Fisher's exact test on the pairs.

    python -m eval.stats results/2026-11-08                                   # -> results/2026-11-08/stats.md
    python -m eval.stats results/2026-11-08 --ablation results/2026-11-08-ablation-mechanism

Reads scores.csv (run eval.grade first). Pass = strict. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

# (control, treatment, what differs). Case ids by number prefix.
PAIRS = [
    ("16", "11", "list, llama-server: temperature 0.7 -> 3.5"),
    ("17", "15", "code, llama-server: temperature 0.7 -> 3.5"),
    ("20", "19", "list, transformers: temperature=3.5 added under do_sample=False"),
    ("22", "21", "code, transformers: temperature=3.5 added under do_sample=False"),
    ("11", "23", "case 11 + the server's default settings and sampler order"),
    ("15", "24", "case 15 + the server's default settings and sampler order"),
]
DECOYS = ("11", "13", "15")


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    """Wilson score interval for k successes in n trials."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def fisher_exact(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p-value for the 2x2 table [[a, b], [c, d]] (sum of tables no more likely than observed)."""
    r1, r2, c1, n = a + b, c + d, a + c, a + b + c + d

    def prob(x: int) -> float:
        return math.comb(r1, x) * math.comb(r2, c1 - x) / math.comb(n, c1)

    p_obs = prob(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs * (1 + 1e-9)))


def load(run_dir: Path) -> list[dict]:
    return list(csv.DictReader((run_dir / "scores.csv").open(encoding="utf-8")))


def _count(rows: list[dict], prefixes: tuple[str, ...]) -> tuple[int, int]:
    sel = [r for r in rows if r["case_id"][:2] in prefixes]
    return sum(r["strict"] == "True" for r in sel), len(sel)


def _fmt(k: int, n: int) -> str:
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({k / n:.0%}, 95% CI {lo:.0%}-{hi:.0%})" if n else "-"


def _p(p: float) -> str:
    return f"{p:.1e}" if p < 1e-3 else f"{p:.3f}"


def report(run_dir: Path, ablation: Path | None = None) -> str:
    rows = load(run_dir)
    L = [f"# Statistics: {run_dir.name}", "", "Pass = strict. Intervals are Wilson 95%; p-values are two-sided Fisher exact.",
         "", "## Pass rate per model", "", "| model | all cases | decoy cases (11, 13, 15) |", "|---|---|---|"]
    for m in sorted({r["model"] for r in rows}):
        rs = [r for r in rows if r["model"] == m]
        k, n = sum(r["strict"] == "True" for r in rs), len(rs)
        L.append(f"| {m} | {_fmt(k, n)} | {_fmt(*_count(rs, DECOYS))} |")
    L += ["", "## Pairs (all models pooled)", "", "| pair | what differs | control | treatment | p |", "|---|---|---|---|---|"]
    for ctrl, treat, what in PAIRS:
        k1, n1 = _count(rows, (ctrl,))
        k2, n2 = _count(rows, (treat,))
        if not n1 or not n2:
            continue
        p = fisher_exact(k1, n1 - k1, k2, n2 - k2)
        L.append(f"| {ctrl} -> {treat} | {what} | {_fmt(k1, n1)} | {_fmt(k2, n2)} | {_p(p)} |")
    if ablation:
        ab = load(ablation)
        L += ["", f"## Ablation: {ablation.name} vs the base prompt (same cases, same models)", "",
              "| case | base prompt | with the extra instruction | p |", "|---|---|---|---|"]
        for cid in sorted({r["case_id"][:2] for r in ab}):
            k1, n1 = _count(rows, (cid,))
            k2, n2 = _count(ab, (cid,))
            p = fisher_exact(k1, n1 - k1, k2, n2 - k2)
            L.append(f"| {cid} | {_fmt(k1, n1)} | {_fmt(k2, n2)} | {_p(p)} |")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--ablation", type=Path, help="a run of the same models with a prompt variant")
    args = ap.parse_args(argv)
    out = args.run_dir / "stats.md"
    out.write_text(report(args.run_dir, args.ablation), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
