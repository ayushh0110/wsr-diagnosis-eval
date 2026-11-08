"""End to end with the mock models: no key, no network."""
import csv
import json
from pathlib import Path

from eval.run import main

FIXTURES = Path(__file__).parent / "fixtures" / "cases"


def test_mock_run_grades_oracle_full_and_naive_zero(tmp_path):
    assert main(["--mock", "--cases", str(FIXTURES), "--runs", "2", "--results", str(tmp_path), "--name", "t"]) == 0
    run = tmp_path / "t"
    rows = list(csv.DictReader((run / "scores.csv").open(encoding="utf-8")))
    assert len(rows) == 4
    oracle = [r for r in rows if r["model"] == "mock/oracle"]
    naive = [r for r in rows if r["model"] == "mock/naive-finetune"]
    assert all(float(r["score"]) == 1.0 for r in oracle)
    assert all(float(r["score"]) == 0.0 and r["overreach"] == "True" for r in naive)
    assert (run / "summary.md").exists() and json.loads((run / "summary.json").read_text())
    # resume: a second invocation makes no new calls and keeps the files
    assert main(["--mock", "--cases", str(FIXTURES), "--runs", "2", "--results", str(tmp_path), "--name", "t"]) == 0
    assert len(list((run / "raw").glob("*.json"))) == 4


def test_transcripts_show_prompt_key_and_every_reply(tmp_path):
    from eval.transcripts import write_transcripts
    assert main(["--mock", "--cases", str(FIXTURES), "--runs", "1", "--results", str(tmp_path), "--name", "t"]) == 0
    out = write_transcripts(tmp_path / "t", FIXTURES)
    page = (out / "fx_penalty.md").read_text(encoding="utf-8")
    assert "FIXTURE_USER_REPORT" in page and "## Prompt" in page and "differ from today's prompt" not in page
    assert "mock/oracle, trial 1: PASS" in page and "mock/naive-finetune, trial 1: fail" in page
    assert "fx_penalty.md" in (out / "README.md").read_text(encoding="utf-8")


def test_api_errors_are_not_graded_as_answers(tmp_path):
    from eval.grade import grade_run
    assert main(["--mock", "--cases", str(FIXTURES), "--runs", "1", "--results", str(tmp_path), "--name", "t"]) == 0
    raw = next((tmp_path / "t" / "raw").glob("*oracle*.json"))
    rec = json.loads(raw.read_text(encoding="utf-8"))
    rec.update(final_content=None, attempts=[{"response": None, "error": "HTTP 429: quota"}])
    raw.write_text(json.dumps(rec), encoding="utf-8")
    rows = grade_run(tmp_path / "t", FIXTURES)
    assert [r["model"] for r in rows] == ["mock/naive-finetune"]   # the errored call is skipped, not scored 0


def test_reply_with_null_content_is_graded_not_skipped(monkeypatch):
    # a provider can answer with "content": null (e.g. the whole budget spent on thinking); that is the model's answer
    import eval.run as run
    from eval.cases import load_case, load_codes
    from eval.grade import parse_response, score_answer
    monkeypatch.setattr(run, "call_model", lambda *a, **k: {"request": {}, "response": {
        "model": "x", "choices": [{"message": {"content": None}, "finish_reason": "length"}]}})
    case = load_case(FIXTURES / "fx_penalty")
    rec = run.run_one(case, {"id": "provider/x", "temperature": 0}, 1, load_codes(), 100)
    assert rec["final_content"] == "" and len(rec["attempts"]) == 2          # graded input, and the format retry ran
    assert score_answer(parse_response(rec["final_content"]), case.key, load_codes())["format_failure"]
