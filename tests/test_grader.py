"""The grader must not give false passes or false fails. Fixture: tests/fixtures/cases/fx_penalty (synthetic)."""
import copy
import json
from pathlib import Path

import pytest

from eval.cases import CASES_DIR, load_case, load_cases, load_codes
from eval.grade import fix_matches, parse_response, score_answer

FX = load_case(Path(__file__).parent / "fixtures" / "cases" / "fx_penalty")
CODES = load_codes()
KEY = FX.key


def ans(verdict="sampling", cause="REPEAT_PENALTY_HIGH", action="set_param", target="repeat_penalty", value=1.0):
    return {"verdict": verdict, "cause": cause, "fix": {"action": action, "target": target, "value": value},
            "rationale": "x"}


def test_golden_answer_scores_full():
    s = score_answer(ans(), KEY, CODES)
    assert s["score"] == 1.0 and s["strict"] and not s["inconsistent"]


@pytest.mark.parametrize("a", [
    ans(target="repetition_penalty"), ans(target="Repeat Penalty"), ans(value="1.05"), ans(value="1.0 (off)"),
    ans(action="remove_param", target="repeat_penalty", value=None),
    ans(verdict="Sampling", cause="repeat-penalty high"),
])
def test_equivalent_spellings_pass(a):
    assert score_answer(a, KEY, CODES)["strict"], a


@pytest.mark.parametrize("a,expect", [
    (ans(verdict="quantisation", cause="LOW_BIT_QUANT_DAMAGE", action="change_quant", target=None, value="Q8_0"), 0.0),
    (ans(value=1.5), 0.8),                              # right cause, penalty still too high
    (ans(target="temperature", value=0.7), 0.8),        # right cause, wrong parameter
    (ans(cause="FREQ_PRESENCE_PENALTY_EXTREME"), 0.6),  # right category, wrong code, fix still right
    (ans(action="raise_max_tokens", target=None, value=4096), 0.8),
])
def test_wrong_answers_lose_the_right_amount(a, expect):
    assert score_answer(a, KEY, CODES)["score"] == pytest.approx(expect)


def test_value_needed_when_range_given():
    assert not fix_matches({"action": "set_param", "target": "repeat_penalty", "value": None},
                           KEY["acceptable_fixes"][:1])


def test_bool_is_not_a_number():
    assert not fix_matches({"action": "set_param", "target": "repeat_penalty", "value": True},
                           KEY["acceptable_fixes"][:1])


def test_overreach_flag():
    s = score_answer(ans(verdict="weight_level", cause="WEIGHT_OTHER", action="weight_edit_or_finetune"), KEY, CODES)
    assert s["overreach"] and s["score"] == 0.0
    # right diagnosis but prescribing a fine-tune anyway is also overreach
    assert score_answer(ans(action="weight_edit_or_finetune"), KEY, CODES)["overreach"]


def test_underreach_and_overclaim_flags():
    wk = copy.deepcopy(KEY)
    wk.update(verdict="weight_level", acceptable_verdicts=["weight_level"], acceptable_causes=["WEIGHT_OVER_REFUSAL"])
    assert score_answer(ans(), wk, CODES)["underreach"]
    ik = copy.deepcopy(KEY)
    ik.update(verdict="inconclusive", acceptable_verdicts=["inconclusive"])
    assert score_answer(ans(), ik, CODES)["overclaim"]


def test_inconsistent_and_invalid_flags():
    s = score_answer(ans(verdict="config"), KEY, CODES)
    assert s["inconsistent"] and not s["verdict_ok"]
    s = score_answer(ans(cause="MADE_UP_CODE", verdict="vibes", action="pray"), KEY, CODES)
    assert s["invalid_code"] and s["invalid_verdict"] and s["invalid_action"] and s["score"] == 0.0


def test_unparseable_is_a_format_failure_not_a_crash():
    s = score_answer(parse_response("I think it's the penalty."), KEY, CODES)
    assert s["format_failure"] and s["score"] == 0.0


@pytest.mark.parametrize("text", [
    json.dumps(ans()),
    "Here is my diagnosis:\n```json\n" + json.dumps(ans()) + "\n```",
    "Thinking... {not json} then " + json.dumps(ans()) + " done.",
])
def test_parse_variants(text):
    assert parse_response(text)["cause"] == "REPEAT_PENALTY_HIGH"


def test_fix_as_bare_string():
    a = ans()
    a["fix"] = "remove_param"
    s = score_answer(a, KEY, CODES)
    assert s["fix_action"] == "remove_param" and not s["fix_ok"]   # no target -> pattern fails


# ---- every real case's key must be consistent with the closed lists

REAL = [c for c in load_cases(CASES_DIR) if c.key]


@pytest.mark.parametrize("case", REAL, ids=[c.id for c in REAL])
def test_real_keys_are_valid_and_golden_passes(case):
    k = case.key
    assert k["verdict"] in CODES["verdicts"] and k["verdict"] in k["acceptable_verdicts"]
    for c in k["acceptable_causes"]:
        assert c in CODES["by_code"], c
    assert k["primary_cause"] in k["acceptable_causes"]
    for f in k["acceptable_fixes"]:
        assert f["action"] in CODES["fix_actions"], f
    golden = {"verdict": k["verdict"], "cause": k["primary_cause"], "fix": k["golden_fix"], "rationale": ""}
    assert score_answer(golden, k, CODES)["strict"], "golden answer must pass its own key"
    for art in case.meta["artifacts"]:
        assert (case.dir / art["path"]).exists(), art


# ---- adversarial answers on the real keys: every tempting distractor must fail, every equivalent phrasing pass

DISTRACTOR_PAIRS = [(c, d) for c in REAL for d in c.key.get("distractors", {})]


@pytest.mark.parametrize("case,code", DISTRACTOR_PAIRS, ids=[f"{c.id}-{d}" for c, d in DISTRACTOR_PAIRS])
def test_distractor_answer_is_not_a_pass(case, code):
    cat = CODES["by_code"][code]["category"]
    a = {"verdict": cat, "cause": code, "fix": dict(case.key["golden_fix"]), "rationale": "distractor"}
    s = score_answer(a, case.key, CODES)
    assert not s["cause_ok"] and not s["strict"] and s["score"] <= 0.6, (case.id, code, s)


EQUIVALENT = [
    ("01_token_salad", {"verdict": "sampling", "cause": "TEMPERATURE_HIGH",
                        "fix": {"action": "set_param", "target": "temperature", "value": "0.8"}}),
    ("02_stop_too_broad", {"verdict": "request", "cause": "STOP_TOO_BROAD",
                           "fix": {"action": "change_stop", "target": "stop", "value": "[]"}}),
    ("03_image_field_ignored", {"verdict": "request", "cause": "IMAGE_FIELD_IGNORED",
                                "fix": {"action": "change_request_format", "target": "content", "value": "image_url part"}}),
    ("04_penalty_script_swap", {"verdict": "sampling", "cause": "REPEAT_PENALTY_HIGH",
                                "fix": {"action": "set_param", "target": "repeat_penalty", "value": 1.05}}),
    ("06_thinking_exhaustion", {"verdict": "request", "cause": "REASONING_STARVES_ANSWER",
                                "fix": {"action": "raise_max_tokens", "target": "max_tokens", "value": 4096}}),
    ("06_thinking_exhaustion", {"verdict": "request", "cause": "REASONING_STARVES_ANSWER",
                                "fix": {"action": "set_param", "target": "chat_template_kwargs.enable_thinking", "value": False}}),
    ("07_greedy_loop_ukrainian", {"verdict": "sampling", "cause": "GREEDY_DECODING_LOOP",
                                  "fix": {"action": "set_param", "target": "do_sample", "value": "true"}}),
    ("08_parse_error_high_temp", {"verdict": "sampling", "cause": "TEMPERATURE_HIGH",
                                  "fix": {"action": "remove_param", "target": "temperature", "value": None}}),
    ("10_inconclusive_cut", {"verdict": "inconclusive", "cause": "INSUFFICIENT_EVIDENCE",
                             "fix": {"action": "raise_max_tokens", "target": "max_new_tokens", "value": 1024}}),
]
BY_ID = {c.id: c for c in REAL}


@pytest.mark.parametrize("cid,a", [e for e in EQUIVALENT if e[0] in BY_ID], ids=[e[0] for e in EQUIVALENT if e[0] in BY_ID])
def test_equivalent_real_answers_pass(cid, a):
    assert score_answer(a, BY_ID[cid].key, CODES)["strict"], (cid, a)


NEAR_MISS = [  # right diagnosis, fix that would not work: loses only the fix credit
    ("04_penalty_script_swap", {"verdict": "sampling", "cause": "REPEAT_PENALTY_HIGH",
                                "fix": {"action": "set_param", "target": "repeat_penalty", "value": 1.5}}, 0.8),
    ("06_thinking_exhaustion", {"verdict": "request", "cause": "REASONING_STARVES_ANSWER",
                                "fix": {"action": "raise_max_tokens", "target": "max_tokens", "value": 300}}, 0.8),
    ("09_overrefusal_weight", {"verdict": "weight_level", "cause": "WEIGHT_OVER_REFUSAL",
                               "fix": {"action": "use_sampling", "target": None, "value": None}}, 0.8),
    ("10_inconclusive_cut", {"verdict": "sampling", "cause": "GREEDY_DECODING_LOOP",
                             "fix": {"action": "use_sampling", "target": None, "value": None}}, 0.0),
]


@pytest.mark.parametrize("cid,a,expect", [e for e in NEAR_MISS if e[0] in BY_ID], ids=[e[0] for e in NEAR_MISS if e[0] in BY_ID])
def test_near_misses_lose_the_right_amount(cid, a, expect):
    assert score_answer(a, BY_ID[cid].key, CODES)["score"] == pytest.approx(expect)


def test_invalid_outer_json_with_valid_inner_object_is_unparseable():
    # a reply missing a comma after "fix": the inner fix object alone must not be graded as the answer
    bad = '{"verdict": "request", "cause": "X", "fix": {"action": "change_request_format"}\n "rationale": "r"}'
    assert parse_response(bad) is None


@pytest.mark.parametrize("value,ok", [
    ("reduce it from 1.5 to 1.0", True), ("1.0 (default)", True), (1.05, True),
    ("1.5", False), ("keep 1.5 or 2.0", False), ("lower it", False),
])
def test_fix_value_counts_any_number_in_range(value, ok):
    spec = [{"action": "set_param", "target_pattern": "repeat|repetition", "value": {"max": 1.15}}]
    assert fix_matches({"action": "set_param", "target": "repeat_penalty", "value": value}, spec) is ok
