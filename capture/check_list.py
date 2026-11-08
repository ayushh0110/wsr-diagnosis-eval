"""Cases 11, 16, 18 evidence: does each captured reply contain exactly the lines 1 to 30, in order?

Lines that are only a number are kept; preambles and code fences are ignored. Writes evidence/list_check.json.

  python capture/check_list.py cases/16_penalty_no_decoy/evidence
"""
import json
import re
import sys
from pathlib import Path


def is_list_1_to_30(text: str) -> bool:
    nums = [line.strip() for line in (text or "").splitlines() if re.fullmatch(r"\s*\d+\s*", line)]
    return nums == [str(i) for i in range(1, 31)]


def reply_text(rec: dict) -> str:
    """The reply in a capture record: llama_server_ab.py (response JSON) or hf_user_script.py (stdout)."""
    if "stdout" in rec:
        return rec["stdout"]
    resp = rec.get("response")
    return resp["choices"][0]["message"]["content"] or "" if isinstance(resp, dict) and resp.get("choices") else ""


def main(ev: Path) -> None:
    rows = []
    for f in sorted([*ev.glob("*_r[0-9]*.json"), *ev.glob("*_seed*.json")]):
        d = json.loads(f.read_text(encoding="utf-8"))
        text = reply_text(d)
        rows.append({"file": f.name, "http": d.get("http_status"), "correct_1_to_30_list": is_list_1_to_30(text)})
        print(f.name, "CORRECT" if rows[-1]["correct_1_to_30_list"] else "broken")
    (ev / "list_check.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
