"""Nothing from the answer key, evidence, title or tier may reach the model."""
from pathlib import Path

import pytest

from eval.cases import CASES_DIR, load_case, load_cases, load_codes
from eval.prompt import build_messages

CODES = load_codes()
FX = load_case(Path(__file__).parent / "fixtures" / "cases" / "fx_penalty")


def text(case):
    return "\n".join(m["content"] for m in build_messages(case, CODES))


def test_prompt_has_report_artifacts_and_lists():
    t = text(FX)
    assert "FIXTURE_USER_REPORT" in t and "FIXTURE_ARTIFACT_TEXT" in t
    assert all(c["code"] in t for c in CODES["codes"])
    assert all(a in t for a in CODES["fix_actions"])


def test_prompt_leaks_nothing_from_the_key():
    t = text(FX)
    for secret in ("SECRET_DISTRACTOR_NOTE", "SECRET_PROVENANCE", "SECRET_EVIDENCE_REPLY",
                   "SYNTHETIC test fixture", "red_herring", "golden_fix", "acceptable_"):
        assert secret not in t, secret


REAL = [c for c in load_cases(CASES_DIR) if c.key]


@pytest.mark.parametrize("case", REAL, ids=[c.id for c in REAL])
def test_real_prompts_leak_no_key_text(case):
    t = text(case)
    assert case.meta["title"] not in t
    k = case.key
    for note in list(k.get("distractors", {}).values()) + [k["provenance"].get("description", "")]:
        if len(note) > 20:
            assert note not in t
    listed = {a["path"] for a in case.meta["artifacts"]}
    shown = {(case.dir / p).read_text(encoding="utf-8", errors="replace").strip() for p in listed}
    ev_dir = case.dir / "evidence"
    for ev in ev_dir.rglob("*") if ev_dir.exists() else []:
        if not ev.is_file() or ev.suffix.lower() not in (".json", ".md", ".txt"):
            continue
        rel = ev.relative_to(case.dir).as_posix()
        body = ev.read_text(encoding="utf-8", errors="replace").strip()
        if rel not in listed and body not in shown and len(body) > 40:  # a copy of a shown file is not a leak
            assert body[:200] not in t, f"evidence {rel} appears in the prompt"


def test_prompt_variant_only_appends_one_instruction():
    from eval.prompt import SYSTEM, VARIANTS, prompt_version
    base, mech = build_messages(FX, CODES), build_messages(FX, CODES, "mechanism")
    assert base[0]["content"] == SYSTEM and base[1] == mech[1]            # the base prompt is untouched
    assert mech[0]["content"] == SYSTEM + "\n" + VARIANTS["mechanism"]   # the variant adds exactly one line
    assert prompt_version() == "1" and prompt_version("mechanism") == "1+mechanism"
