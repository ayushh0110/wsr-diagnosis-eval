"""Run a user's transformers script verbatim (several seeds) and a one-line variant, saving every output.

Used for case 14, where the bug is in what the script does NOT set, so the artifact shown to the model is the
script itself (user_script.py), exactly as executed. Each run executes the script text with exec() after
torch.manual_seed(seed) and captures what it prints and any warnings. The variant is the same script with one
textual replacement (--variant NAME "OLD" "NEW"), so the flip is a single-line change.

  python capture/hf_user_script.py --case-dir cases/14_hf_default_length --script capture/args/14_user_script.py \
    --seeds 1-3 --variant max_new_tokens "model.generate(**inputs)" "model.generate(**inputs, max_new_tokens=300)"
"""
from __future__ import annotations

import argparse
import contextlib
import io
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import env_info, write_json, write_text  # noqa: E402


def run_script(src: str, seed: int) -> dict:
    import torch
    torch.manual_seed(seed)
    buf = io.StringIO()
    t0 = time.time()
    with warnings.catch_warnings(record=True) as w, contextlib.redirect_stdout(buf):
        warnings.simplefilter("always")
        exec(compile(src, "user_script.py", "exec"), {"__name__": "__main__"})
    return {"seed": seed, "stdout": buf.getvalue(), "warnings": sorted({str(x.message)[:300] for x in w}),
            "seconds": round(time.time() - t0, 1)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--case-dir", type=Path, required=True)
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--seeds", default="1-3")
    ap.add_argument("--variant", nargs=3, action="append", default=[], metavar=("NAME", "OLD", "NEW"))
    args = ap.parse_args(argv)
    a, _, b = args.seeds.partition("-")
    seeds = list(range(int(a), int(b or a) + 1))
    src = args.script.read_text(encoding="utf-8")
    arms = [("failing", src)]
    for name, old, new in args.variant:
        assert old in src, f"{old!r} not in script"
        arms.append((name, src.replace(old, new)))
    case, ev = args.case_dir, args.case_dir / "evidence"
    lines = [f"# Capture summary: {case.name}", "", "| arm | seed | seconds | output |", "|---|---|---|---|"]
    first = None
    for name, s in arms:
        write_text(ev / f"{name}_script.py", s)
        for seed in seeds:
            rec = run_script(s, seed)
            rec["arm"] = name
            write_json(ev / f"{name}_seed{seed}.json", rec)
            out = rec["stdout"].strip().replace("\n", " \\n ").replace("|", "\\|")
            lines.append(f"| {name} | {seed} | {rec['seconds']} | {out[:200]} |")
            print(f"{name} seed {seed}: {len(rec['stdout'])} chars, {rec['seconds']} s")
            if first is None:
                first = rec
    import torch
    import transformers
    write_json(ev / "env.json", env_info({"script": "hf_user_script.py", "torch": torch.__version__,
                                          "transformers": transformers.__version__, "seeds": seeds,
                                          "arms": [n for n, _ in arms]}))
    write_text(ev / "summary.md", "\n".join(lines) + "\n")
    write_text(case / "user_script.py", src)
    write_text(case / "output.txt", first["stdout"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
