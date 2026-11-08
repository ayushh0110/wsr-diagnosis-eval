# Statistics: 2026-11-08

Pass = strict. Intervals are Wilson 95%; p-values are two-sided Fisher exact.

## Pass rate per model

| model | all cases | decoy cases (11, 13, 15) |
|---|---|---|
| gemini/gemini-3.8-flash | 59/72 (82%, 95% CI 72%-89%) | 1/9 (11%, 95% CI 2%-43%) |
| gemini/gemini-4-argon | 63/72 (88%, 95% CI 78%-93%) | 3/9 (33%, 95% CI 12%-65%) |
| kiro/claude-opus-5.5 | 68/72 (94%, 95% CI 87%-98%) | 5/9 (56%, 95% CI 27%-81%) |
| kiro/claude-sonnet-5.5 | 67/72 (93%, 95% CI 85%-97%) | 4/9 (44%, 95% CI 19%-73%) |
| kiro/gpt-5.6-sol | 57/72 (79%, 95% CI 68%-87%) | 0/9 (0%, 95% CI 0%-30%) |
| kiro/kimi-k3 | 57/72 (79%, 95% CI 68%-87%) | 0/9 (0%, 95% CI 0%-30%) |

## Pairs (all models pooled)

| pair | what differs | control | treatment | p |
|---|---|---|---|---|
| 16 -> 11 | list, llama-server: temperature 0.7 -> 3.5 | 18/18 (100%, 95% CI 82%-100%) | 0/18 (0%, 95% CI 0%-18%) | 2.2e-10 |
| 17 -> 15 | code, llama-server: temperature 0.7 -> 3.5 | 18/18 (100%, 95% CI 82%-100%) | 4/18 (22%, 95% CI 9%-45%) | 1.6e-06 |
| 20 -> 19 | list, transformers: temperature=3.5 added under do_sample=False | 18/18 (100%, 95% CI 82%-100%) | 18/18 (100%, 95% CI 82%-100%) | 1.000 |
| 22 -> 21 | code, transformers: temperature=3.5 added under do_sample=False | 18/18 (100%, 95% CI 82%-100%) | 18/18 (100%, 95% CI 82%-100%) | 1.000 |
| 11 -> 23 | case 11 + the server's default settings and sampler order | 0/18 (0%, 95% CI 0%-18%) | 6/18 (33%, 95% CI 16%-56%) | 0.019 |
| 15 -> 24 | case 15 + the server's default settings and sampler order | 4/18 (22%, 95% CI 9%-45%) | 10/18 (56%, 95% CI 34%-75%) | 0.086 |

## Ablation: 2026-11-08-ablation-mechanism vs the base prompt (same cases, same models)

| case | base prompt | with the extra instruction | p |
|---|---|---|---|
| 11 | 0/18 (0%, 95% CI 0%-18%) | 9/18 (50%, 95% CI 29%-71%) | 0.001 |
| 13 | 9/18 (50%, 95% CI 29%-71%) | 12/18 (67%, 95% CI 44%-84%) | 0.500 |
| 15 | 4/18 (22%, 95% CI 9%-45%) | 11/18 (61%, 95% CI 39%-80%) | 0.041 |
| 18 | 18/18 (100%, 95% CI 82%-100%) | 18/18 (100%, 95% CI 82%-100%) | 1.000 |
