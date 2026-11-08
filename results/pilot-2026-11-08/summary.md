# Results: pilot-2026-11-08

## Per model

| model | runs | mean | strict | control | red_herring | dont_blame_weights | blame_weights | inconclusive | overreach | underreach | overclaim | took the decoy | format fail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kiro/claude-opus-5.5 | 10 | 1.00 | 100% | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/9 | 0/1 | 0/1 | 0/10 | 0 |
| kiro/claude-sonnet-5.5 | 10 | 1.00 | 100% | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/9 | 0/1 | 0/1 | 0/10 | 0 |
| kiro/gpt-5.6-sol | 10 | 1.00 | 100% | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/9 | 0/1 | 0/1 | 0/10 | 0 |
| kiro/kimi-k3 | 10 | 1.00 | 100% | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0/9 | 0/1 | 0/1 | 0/10 | 0 |

Overreach: blamed the weights (or prescribed a weight edit / fine-tune) on a non-weight case. Underreach: blamed a setting on a weight-level case. Overclaim: named a cause on an inconclusive case.

## Consistency over trials

Pass = strict (verdict, cause and fix all right). pass@k: the case was passed in at least one of k trials; pass^k: in all k.

| model | cases | trials per case (k) | pass rate (per trial) | pass@k | pass^k |
|---|---|---|---|---|---|
| kiro/claude-opus-5.5 | 10 | 1 | 100% | 100% | 100% |
| kiro/claude-sonnet-5.5 | 10 | 1 | 100% | 100% | 100% |
| kiro/gpt-5.6-sol | 10 | 1 | 100% | 100% | 100% |
| kiro/kimi-k3 | 10 | 1 | 100% | 100% | 100% |

## Per case (strict passes / trials)

| case | tier | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|
| 01_token_salad | control | 1/1 | 1/1 | 1/1 | 1/1 |
| 02_stop_too_broad | control | 1/1 | 1/1 | 1/1 | 1/1 |
| 03_image_field_ignored | control | 1/1 | 1/1 | 1/1 | 1/1 |
| 04_penalty_script_swap | red_herring | 1/1 | 1/1 | 1/1 | 1/1 |
| 05_penalty_shape_loss | red_herring | 1/1 | 1/1 | 1/1 | 1/1 |
| 06_thinking_exhaustion | red_herring | 1/1 | 1/1 | 1/1 | 1/1 |
| 07_greedy_loop_ukrainian | dont_blame_weights | 1/1 | 1/1 | 1/1 | 1/1 |
| 08_parse_error_high_temp | red_herring | 1/1 | 1/1 | 1/1 | 1/1 |
| 09_overrefusal_weight | blame_weights | 1/1 | 1/1 | 1/1 | 1/1 |
| 10_inconclusive_cut | inconclusive | 1/1 | 1/1 | 1/1 | 1/1 |

## Per case (mean score over runs)

| case | tier | kiro/claude-opus-5.5 | kiro/claude-sonnet-5.5 | kiro/gpt-5.6-sol | kiro/kimi-k3 |
|---|---|---|---|---|---|
| 01_token_salad | control | 1.00 | 1.00 | 1.00 | 1.00 |
| 02_stop_too_broad | control | 1.00 | 1.00 | 1.00 | 1.00 |
| 03_image_field_ignored | control | 1.00 | 1.00 | 1.00 | 1.00 |
| 04_penalty_script_swap | red_herring | 1.00 | 1.00 | 1.00 | 1.00 |
| 05_penalty_shape_loss | red_herring | 1.00 | 1.00 | 1.00 | 1.00 |
| 06_thinking_exhaustion | red_herring | 1.00 | 1.00 | 1.00 | 1.00 |
| 07_greedy_loop_ukrainian | dont_blame_weights | 1.00 | 1.00 | 1.00 | 1.00 |
| 08_parse_error_high_temp | red_herring | 1.00 | 1.00 | 1.00 | 1.00 |
| 09_overrefusal_weight | blame_weights | 1.00 | 1.00 | 1.00 | 1.00 |
| 10_inconclusive_cut | inconclusive | 1.00 | 1.00 | 1.00 | 1.00 |

## Most common wrong causes

| case | wrong cause | count | models |
|---|---|---|---|
