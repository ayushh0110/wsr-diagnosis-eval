# Results: 2026-11-08

## Per model

| model | runs | mean | strict | control | red_herring | decoy_setting | decoy_documented | decoy_twin | decoy_reverse | dont_blame_weights | blame_weights | inconclusive | overreach | underreach | overclaim | took the decoy | format fail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini/gemini-3.8-flash | 72 | 0.89 | 82% | 1.00 | 1.00 | 0.68 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/69 | 0/3 | 0/3 | 13/72 | 0 |
| gemini/gemini-4-argon | 72 | 0.88 | 88% | 1.00 | 1.00 | 0.60 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/69 | 0/3 | 0/3 | 0/72 | 0 |
| kiro/claude-opus-5.5 | 72 | 0.97 | 94% | 1.00 | 1.00 | 0.84 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/69 | 0/3 | 0/3 | 4/72 | 0 |
| kiro/claude-sonnet-5.5 | 72 | 0.96 | 93% | 1.00 | 1.00 | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/69 | 0/3 | 0/3 | 5/72 | 0 |
| kiro/gpt-5.6-sol | 72 | 0.87 | 79% | 1.00 | 1.00 | 0.61 | 0.40 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/69 | 0/3 | 0/3 | 14/72 | 0 |
| kiro/kimi-k3 | 72 | 0.88 | 79% | 1.00 | 1.00 | 0.64 | 0.40 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/69 | 0/3 | 0/3 | 15/72 | 0 |

Overreach: blamed the weights (or prescribed a weight edit / fine-tune) on a non-weight case. Underreach: blamed a setting on a weight-level case. Overclaim: named a cause on an inconclusive case.

## Consistency over trials

Pass = strict (verdict, cause and fix all right). pass@k: the case was passed in at least one of k trials; pass^k: in all k.

| model | cases | trials per case (k) | pass rate (per trial) | pass@k | pass^k |
|---|---|---|---|---|---|
| gemini/gemini-3.8-flash | 24 | 3 | 82% | 88% | 79% |
| gemini/gemini-4-argon | 24 | 3 | 88% | 88% | 88% |
| kiro/claude-opus-5.5 | 24 | 3 | 94% | 96% | 92% |
| kiro/claude-sonnet-5.5 | 24 | 3 | 93% | 96% | 92% |
| kiro/gpt-5.6-sol | 24 | 3 | 79% | 79% | 79% |
| kiro/kimi-k3 | 24 | 3 | 79% | 79% | 79% |

## Per case (strict passes / trials)

| case | tier | gemini/gemini-3.8-flash | gemini/gemini-4-argon | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|---|---|
| 01_token_salad | control | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 02_stop_too_broad | control | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 03_image_field_ignored | control | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 04_penalty_script_swap | red_herring | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 05_penalty_shape_loss | red_herring | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 06_thinking_exhaustion | red_herring | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 07_greedy_loop_ukrainian | dont_blame_weights | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 08_parse_error_high_temp | red_herring | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 09_overrefusal_weight | blame_weights | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 10_inconclusive_cut | inconclusive | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 11_penalty_temperature_decoy | decoy_setting | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| 12_prompt_cache_nondeterminism | red_herring | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 13_server_penalty_buried | decoy_setting | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| 14_hf_default_length | red_herring | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 15_code_temperature_decoy | decoy_setting | 1/3 | 0/3 | 2/3 | 1/3 | 0/3 | 0/3 |
| 16_penalty_no_decoy | decoy_twin | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 17_code_penalty_no_decoy | decoy_twin | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 18_temperature_guilty_penalty_innocent | decoy_reverse | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 19_hf_greedy_temperature_ignored | decoy_setting | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 20_hf_penalty_no_decoy | decoy_twin | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 21_hf_code_greedy_temperature_ignored | decoy_setting | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 22_hf_code_penalty_no_decoy | decoy_twin | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 23_penalty_temperature_decoy_with_server_defaults | decoy_documented | 0/3 | 0/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| 24_code_temperature_decoy_with_server_defaults | decoy_documented | 1/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |

## Per case (mean score over runs)

| case | tier | gemini/gemini-3.8-flash | gemini/gemini-4-argon | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|---|---|
| 01_token_salad | control | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 02_stop_too_broad | control | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 03_image_field_ignored | control | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 04_penalty_script_swap | red_herring | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 05_penalty_shape_loss | red_herring | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 06_thinking_exhaustion | red_herring | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 07_greedy_loop_ukrainian | dont_blame_weights | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 08_parse_error_high_temp | red_herring | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 09_overrefusal_weight | blame_weights | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 10_inconclusive_cut | inconclusive | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 11_penalty_temperature_decoy | decoy_setting | 0.40 | 0.00 | 0.40 | 0.40 | 0.40 | 0.40 |
| 12_prompt_cache_nondeterminism | red_herring | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 13_server_penalty_buried | decoy_setting | 0.40 | 1.00 | 1.00 | 1.00 | 0.27 | 0.40 |
| 14_hf_default_length | red_herring | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 15_code_temperature_decoy | decoy_setting | 0.60 | 0.00 | 0.80 | 0.60 | 0.40 | 0.40 |
| 16_penalty_no_decoy | decoy_twin | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 17_code_penalty_no_decoy | decoy_twin | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 18_temperature_guilty_penalty_innocent | decoy_reverse | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 19_hf_greedy_temperature_ignored | decoy_setting | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 20_hf_penalty_no_decoy | decoy_twin | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 21_hf_code_greedy_temperature_ignored | decoy_setting | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 22_hf_code_penalty_no_decoy | decoy_twin | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 23_penalty_temperature_decoy_with_server_defaults | decoy_documented | 0.40 | 0.00 | 1.00 | 1.00 | 0.40 | 0.40 |
| 24_code_temperature_decoy_with_server_defaults | decoy_documented | 0.60 | 1.00 | 1.00 | 1.00 | 0.40 | 0.40 |

## Most common wrong causes

| case | wrong cause | count | models |
|---|---|---|---|
| 11_penalty_temperature_decoy | TEMPERATURE_HIGH | 15 | gemini/gemini-3.8-flash, kiro/claude-opus-5.5, kiro/claude-sonnet-5.5, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 11_penalty_temperature_decoy | INSUFFICIENT_EVIDENCE | 3 | gemini/gemini-4-argon |
| 13_server_penalty_buried | FREQ_PRESENCE_PENALTY_EXTREME | 8 | gemini/gemini-3.8-flash, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 13_server_penalty_buried | INSUFFICIENT_EVIDENCE | 1 | kiro/gpt-5.6-sol |
| 15_code_temperature_decoy | TEMPERATURE_HIGH | 11 | gemini/gemini-3.8-flash, kiro/claude-opus-5.5, kiro/claude-sonnet-5.5, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 15_code_temperature_decoy | INSUFFICIENT_EVIDENCE | 3 | gemini/gemini-4-argon |
| 23_penalty_temperature_decoy_with_server_defaults | TEMPERATURE_HIGH | 9 | gemini/gemini-3.8-flash, kiro/gpt-5.6-sol, kiro/kimi-k3 |
| 23_penalty_temperature_decoy_with_server_defaults | INSUFFICIENT_EVIDENCE | 3 | gemini/gemini-4-argon |
| 24_code_temperature_decoy_with_server_defaults | TEMPERATURE_HIGH | 8 | gemini/gemini-3.8-flash, kiro/gpt-5.6-sol, kiro/kimi-k3 |
