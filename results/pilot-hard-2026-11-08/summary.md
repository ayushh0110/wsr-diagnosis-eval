# Results: pilot-hard-2026-11-08

## Per model

| model | runs | mean | strict | red_herring | decoy_setting | overreach | underreach | overclaim | took the decoy | format fail |
|---|---|---|---|---|---|---|---|---|---|---|
| kiro/claude-opus-5.5 | 5 | 0.88 | 80% | 1.00 | 0.80 | 0/5 | - | - | 1/5 | 0 |
| kiro/claude-sonnet-5.5 | 5 | 1.00 | 100% | 1.00 | 1.00 | 0/5 | - | - | 0/5 | 0 |
| kiro/gpt-5.6-sol | 5 | 0.56 | 40% | 1.00 | 0.27 | 0/5 | - | - | 2/5 | 0 |
| kiro/kimi-k3 | 5 | 0.76 | 60% | 1.00 | 0.60 | 0/5 | - | - | 2/5 | 0 |

Overreach: blamed the weights (or prescribed a weight edit / fine-tune) on a non-weight case. Underreach: blamed a setting on a weight-level case. Overclaim: named a cause on an inconclusive case.

## Consistency over trials

Pass = strict (verdict, cause and fix all right). pass@k: the case was passed in at least one of k trials; pass^k: in all k.

| model | cases | trials per case (k) | pass rate (per trial) | pass@k | pass^k |
|---|---|---|---|---|---|
| kiro/claude-opus-5.5 | 5 | 1 | 80% | 80% | 80% |
| kiro/claude-sonnet-5.5 | 5 | 1 | 100% | 100% | 100% |
| kiro/gpt-5.6-sol | 5 | 1 | 40% | 40% | 40% |
| kiro/kimi-k3 | 5 | 1 | 60% | 60% | 60% |

## Per case (strict passes / trials)

| case | tier | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|
| 11_penalty_temperature_decoy | decoy_setting | 0/1 | 1/1 | 0/1 | 0/1 |
| 12_prompt_cache_nondeterminism | red_herring | 1/1 | 1/1 | 1/1 | 1/1 |
| 13_server_penalty_buried | decoy_setting | 1/1 | 1/1 | 0/1 | 1/1 |
| 14_hf_default_length | red_herring | 1/1 | 1/1 | 1/1 | 1/1 |
| 15_code_temperature_decoy | decoy_setting | 1/1 | 1/1 | 0/1 | 0/1 |

## Per case (mean score over runs)

| case | tier | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|
| 11_penalty_temperature_decoy | decoy_setting | 0.40 | 1.00 | 0.40 | 0.40 |
| 12_prompt_cache_nondeterminism | red_herring | 1.00 | 1.00 | 1.00 | 1.00 |
| 13_server_penalty_buried | decoy_setting | 1.00 | 1.00 | 0.00 | 1.00 |
| 14_hf_default_length | red_herring | 1.00 | 1.00 | 1.00 | 1.00 |
| 15_code_temperature_decoy | decoy_setting | 1.00 | 1.00 | 0.40 | 0.40 |

## Most common wrong causes

| case | wrong cause | count | models |
|---|---|---|---|
| 11_penalty_temperature_decoy | TEMPERATURE_HIGH | 3 | kiro/claude-opus-5.5, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 13_server_penalty_buried | INSUFFICIENT_EVIDENCE | 1 | kiro/gpt-5.6-sol |
| 15_code_temperature_decoy | TEMPERATURE_HIGH | 2 | kiro/gpt-5.6-sol, kiro/kimi-k3 |
