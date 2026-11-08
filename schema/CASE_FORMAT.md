# Case format

Each case is a folder under `cases/` holding:

| File | Shown to the model? | What it holds |
|---|---|---|
| `case.json` | yes (`user_report`, `environment`, listed `artifacts`, `experiments_log`) | the failure as the user experienced it |
| artifact files (`request.json`, `response.json`, `server_cmd.txt`, config excerpts ...) | yes, only those listed in `case.json` | raw captures, never hand-edited |
| `experiments_log.md` (optional) | yes, when `case.json` names it | experiments the user already ran, as a user would report them |
| `answer.json` | **no** | the key: verdict, causes, fixes, distractors, provenance |
| `evidence/` | **no** | the other arm of the flip, reruns, logs that establish the key |

`title` and `tier` in `case.json` are for the report only; `eval/prompt.py` never sends them.

Tiers (`eval/report.py` lists them in this order):

| tier | meaning |
|---|---|
| `control` | an expert solves it at a glance |
| `red_herring` | a tempting wrong cause is present, or the user suggests one |
| `decoy_setting` | two suspicious settings in the artifacts; the louder one is innocent |
| `decoy_documented` | a decoy case with the runtime's own defaults and sampler order added as an artifact |
| `decoy_twin` | a decoy case with only the decoy removed |
| `decoy_reverse` | the same two suspects, but the runtime makes the louder one guilty |
| `dont_blame_weights` | looks like a model defect; a decoding setting causes it |
| `blame_weights` | every setting is neutral and it persists: the weights |
| `inconclusive` | the artifacts can't show the failure; the answer is the next experiment |

Artifacts may also be a user's script and its printed output (`user_script.py`, `output.txt`) when the bug is in
what the script does not set; `capture/hf_user_script.py` runs such a script verbatim.

## Answer key fields

- `acceptable_verdicts`, `acceptable_causes`: every answer an expert would accept. Keep them tight; widen only for a real synonym.
- `acceptable_fixes`: list of `{action, target_pattern?, value?}`. A fix passes if it matches any entry: same `action`, `target_pattern` (case-insensitive regex) found in the answer's target, and `value` within `{min, max}` or matching `{pattern}`.
- `golden_fix`: one concrete fix, used by the oracle mock and the grader tests.
- `distractors`: the tempting wrong causes and why the evidence rules them out (used in the failure analysis).
- `provenance.method`:
  - `one_factor_flip`: one setting changed, the failure disappeared, and both arms reproduced on a rerun.
  - `planted`: the bug was put there on purpose (say so in the README).
  - `persistence`: the failure persists at full precision, greedy and sampled, with a verified template and neutral settings.
  - `truncation`: the reply was cut before the failure could be observed.

## Writing rules (no leaks, no tricks)

1. `user_report` sounds like a user: symptoms and frustration, no cause names, no "I already checked X" unless they did.
2. No wsr finding codes or wsr messages in anything shown to the model.
3. Remove local paths, user names, host names, keys.
4. Never edit a captured reply. If a capture is wrong, capture again.
5. Every distractor must be something actually present in the artifacts (e.g. a real Q4_0 file), not invented noise.
