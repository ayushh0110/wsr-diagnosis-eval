# Results: 2026-11-08-ablation-mechanism

## Per model

| model | runs | mean | strict | decoy_setting | decoy_reverse | overreach | underreach | overclaim | took the decoy | format fail |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini/gemini-3.8-flash | 12 | 0.75 | 58% | 0.67 | 1.00 | 0/12 | - | - | 5/12 | 0 |
| gemini/gemini-4-argon | 12 | 1.00 | 100% | 1.00 | 1.00 | 0/12 | - | - | 0/12 | 0 |
| kiro/claude-opus-5.5 | 12 | 1.00 | 100% | 1.00 | 1.00 | 0/12 | - | - | 0/12 | 0 |
| kiro/claude-sonnet-5.5 | 12 | 1.00 | 100% | 1.00 | 1.00 | 0/12 | - | - | 0/12 | 0 |
| kiro/gpt-5.6-sol | 12 | 0.45 | 25% | 0.27 | 1.00 | 0/12 | - | - | 6/12 | 0 |
| kiro/kimi-k3 | 12 | 0.60 | 33% | 0.47 | 1.00 | 0/12 | - | - | 8/12 | 0 |

Overreach: blamed the weights (or prescribed a weight edit / fine-tune) on a non-weight case. Underreach: blamed a setting on a weight-level case. Overclaim: named a cause on an inconclusive case.

## Consistency over trials

Pass = strict (verdict, cause and fix all right). pass@k: the case was passed in at least one of k trials; pass^k: in all k.

| model | cases | trials per case (k) | pass rate (per trial) | pass@k | pass^k |
|---|---|---|---|---|---|
| gemini/gemini-3.8-flash | 4 | 3 | 58% | 75% | 25% |
| gemini/gemini-4-argon | 4 | 3 | 100% | 100% | 100% |
| kiro/claude-opus-5.5 | 4 | 3 | 100% | 100% | 100% |
| kiro/claude-sonnet-5.5 | 4 | 3 | 100% | 100% | 100% |
| kiro/gpt-5.6-sol | 4 | 3 | 25% | 25% | 25% |
| kiro/kimi-k3 | 4 | 3 | 33% | 50% | 25% |

## Per case (strict passes / trials)

| case | tier | gemini/gemini-3.8-flash | gemini/gemini-4-argon | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|---|---|
| 11_penalty_temperature_decoy | decoy_setting | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| 13_server_penalty_buried | decoy_setting | 2/3 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 |
| 15_code_temperature_decoy | decoy_setting | 2/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| 18_temperature_guilty_penalty_innocent | decoy_reverse | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

## Per case (mean score over runs)

| case | tier | gemini/gemini-3.8-flash | gemini/gemini-4-argon | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|---|---|
| 11_penalty_temperature_decoy | decoy_setting | 0.40 | 1.00 | 1.00 | 1.00 | 0.27 | 0.40 |
| 13_server_penalty_buried | decoy_setting | 0.80 | 1.00 | 1.00 | 1.00 | 0.13 | 0.60 |
| 15_code_temperature_decoy | decoy_setting | 0.80 | 1.00 | 1.00 | 1.00 | 0.40 | 0.40 |
| 18_temperature_guilty_penalty_innocent | decoy_reverse | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

## Most common wrong causes

| case | wrong cause | count | models |
|---|---|---|---|
| 11_penalty_temperature_decoy | TEMPERATURE_HIGH | 8 | gemini/gemini-3.8-flash, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 11_penalty_temperature_decoy | INSUFFICIENT_EVIDENCE | 1 | kiro/gpt-5.6-sol |
| 13_server_penalty_buried | FREQ_PRESENCE_PENALTY_EXTREME | 4 | gemini/gemini-3.8-flash, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 13_server_penalty_buried | INSUFFICIENT_EVIDENCE | 2 | kiro/gpt-5.6-sol |
| 15_code_temperature_decoy | TEMPERATURE_HIGH | 7 | gemini/gemini-3.8-flash, kiro/gpt-5.6-sol, kiro/kimi-k3 |
