# Grader audit (run 2026-11-08)

Purpose: check the deterministic grader for false fails (a right diagnosis scored wrong) and false passes (a
wrong or self-contradicting diagnosis scored right). Done by reading the free-text `rationale` of the answers
against their structured fields and the case's captured evidence. Performed during preparation with an AI coding
assistant (Claude Code) and checked by the author.

## Every non-strict answer (61 of 432)

27 from the four Kiro-run models (table below), then 14 from the two Gemini models (next table).

| case | answers | what they said | verdict on the grading |
|---|---|---|---|
| 11 | 12 (all models, all runs) | `TEMPERATURE_HIGH`, fix: temperature 0.7-1.0 | correct fail: with the penalty kept, temperature 0.7 still breaks the list 4/4 (evidence/temp_07_*) |
| 13 | 5 (GPT-5.6 Sol 2, Kimi K3 3) | `FREQ_PRESENCE_PENALTY_EXTREME`, fix: presence_penalty 0 | correct fail: removing presence_penalty leaves the code broken 3/3 (evidence/presence_off_*) |
| 13 | 1 (GPT-5.6 Sol) | `INSUFFICIENT_EVIDENCE`, fix: 2x2 ablation | correct fail by the key; the most defensible wrong answer in the set (see README, case 13) |
| 15 | 9 | `TEMPERATURE_HIGH`, fix: temperature 0.2-1.0 | correct fail: temperature 0.7 with the penalty kept runs 0/4 (evidence/code_check.json); 0.2 and 1.0 were not captured, but the penalty breaks the code at both 0.7 and 3.5 |

| case | answers (Gemini) | what they said | verdict on the grading |
|---|---|---|---|
| 11 | 3 (3.8 Flash) | `TEMPERATURE_HIGH`, fix: temperature 0.7 | correct fail, as above |
| 11 | 3 (4 Argon) | `inconclusive` / `INSUFFICIENT_EVIDENCE`, fix: reset temperature and repeat_penalty one at a time | correct fail by the key. Defensible as a cautious answer, but its rationale assumes temperature 3.5 "flattens the logits into random token selection", which the fluent reply in the artifacts rules out on llama-server; an expert decides this case from the artifacts |
| 13 | 3 (3.8 Flash) | `FREQ_PRESENCE_PENALTY_EXTREME`, fix: remove presence_penalty | correct fail, as above |
| 15 | 2 (3.8 Flash) | `TEMPERATURE_HIGH`, fix: temperature 0.7 | correct fail, as above |
| 15 | 3 (4 Argon) | `inconclusive`, fix: test the two settings separately | correct fail by the key, same reasoning as case 11 |

Eight Gemini 3.8 Flash calls (from a leftover free-tier-key process) returned HTTP 429 (free-tier daily quota) with no reply. They were never graded:
the grader skips calls without a model reply (`tests/test_pipeline.py::test_api_errors_are_not_graded_as_answers`),
and they were retried on resume.

Cases 19-22 (transformers, added last) have no failed answers. All 36 passes on the two decoy cases (19, 21) were
checked by pattern and by reading a sample: every rationale says temperature is ignored because `do_sample=False`
and names the repetition penalty, so none of them passed by guessing.

Cases 23 and 24 (11 and 15 plus the server's default settings) add 20 failures: 17 `TEMPERATURE_HIGH` with a
temperature fix, and 3 `INSUFFICIENT_EVIDENCE` (Gemini 4 Argon on 23). All 20 were categorised by their structured
fields and 5 were read in full; each is the decoy or the hedge seen on 11 and 15, and is a correct fail for the same
reasons. The ablation run (`results/2026-11-08-ablation-mechanism/`) has 22 failures of the same three kinds
(15 `TEMPERATURE_HIGH`, 4 `FREQ_PRESENCE_PENALTY_EXTREME`, 3 `INSUFFICIENT_EVIDENCE`); a sample of 6 was read.

No answer had the right cause with a rejected fix, so no fix pattern in the keys was too narrow.

## Sample of strict passes (21 of 189)

All 9 strict passes on the decoy cases (13 x6, 15 x3) and 12 random strict passes from the other cases
(`random.seed(7)`): every rationale names the same mechanism as the structured cause and cites evidence that is in
the artifacts (e.g. "for j from range(6) because 'in' was penalised", "cached_tokens 1 vs 28", "stopped on the
end-of-turn token after 92 of 200 tokens"). No pass relied on a guess that contradicted its own rationale.

## Grader bug found and fixed

Sonnet 5.5, case 03, run 2 returned JSON with a missing comma after `fix`. The parser fell back to the first
JSON object it could decode, the inner `fix` object, so the reply was graded as "(no answer)" instead of triggering
the one format retry: a false fail. The parser now accepts only objects with a `verdict` or `cause`
(`tests/test_grader.py::test_invalid_outer_json_with_valid_inner_object_is_unparseable`), and the runner applied the
skipped retry on resume (attempt 2 in that raw file, marked "format retry applied on resume"). It parsed, and the
answer is correct.

Disagreement between grader and audit after the fix: none found (41 failures read in full, 20 + 22 later ones
categorised with 11 read in full, 21 sampled passes).
