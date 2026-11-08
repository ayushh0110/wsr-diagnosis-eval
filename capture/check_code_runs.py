"""Cases 15, 17, 21, 22 evidence: run the Python in every captured reply and record whether it prints the 5x5 table.

Executes code written by the local model under test (a few lines printing a table), in a subprocess with a timeout.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ev = Path(sys.argv[1])
rows = []
for f in sorted([*ev.glob("*_r[0-9]*.json"), *ev.glob("*_seed*.json")]):
    rec = json.loads(f.read_text(encoding="utf-8"))
    t = rec["stdout"] if "stdout" in rec else rec["response"]["choices"][0]["message"]["content"] or ""
    m = re.search(r"```(?:python)?\n(.*?)```", t, re.S)
    code = m.group(1) if m else t
    try:
        p = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=20)
        out, err = p.stdout, p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []
    except subprocess.TimeoutExpired:
        out, err = "", ["timeout"]
    ok = all(str(n) in out for n in (1, 5, 10, 16, 20, 25))
    rows.append({"file": f.name, "prints_5x5_table": ok, "stdout_head": out[:120], "error": err})
    print(f.name, "PRINTS_TABLE" if ok else "FAILS", err)
(ev / "code_check.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
