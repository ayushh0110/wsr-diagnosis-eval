"""Load cases, answer keys and the code list."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
CODES_PATH = ROOT / "schema" / "codes.json"
CASES_DIR = ROOT / "cases"


def load_codes(path: Path = CODES_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["by_code"] = {c["code"]: c for c in data["codes"]}
    return data


@dataclass
class Case:
    id: str
    dir: Path
    meta: dict[str, Any]
    key: Optional[dict[str, Any]]

    @property
    def tier(self) -> str:
        return self.meta.get("tier", "")


def load_case(case_dir: Path) -> Case:
    meta = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
    key_path = case_dir / "answer.json"
    key = json.loads(key_path.read_text(encoding="utf-8")) if key_path.exists() else None
    return Case(id=meta.get("id", case_dir.name), dir=case_dir, meta=meta, key=key)


def load_cases(cases_dir: Path = CASES_DIR, only: Optional[list[str]] = None) -> list[Case]:
    """Every subfolder with a case.json, sorted by name. Folders without one are skipped (work in progress)."""
    out = []
    for d in sorted(p for p in cases_dir.iterdir() if p.is_dir()):
        if not (d / "case.json").exists():
            continue
        c = load_case(d)
        if only and c.id not in only and d.name not in only:
            continue
        out.append(c)
    return out
