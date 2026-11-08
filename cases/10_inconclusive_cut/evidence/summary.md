# Capture summary: 10_inconclusive_cut

Model `Qwen/Qwen2.5-0.5B-Instruct`, fp32 on cuda, max_new_tokens 64. First arm = what the user ran.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| greedy | 1 | `{"seed": null, "system": false}` | none | length | Introducing the Stainless Steel Water Bottle - Your Ultimate Choice for Freshness and Comfort! \n  \n Imagine a bottle t |
| greedy_rerun | 1 | `{"seed": null, "system": false}` | none | length | Introducing the Stainless Steel Water Bottle - Your Ultimate Choice for Freshness and Comfort! \n  \n Imagine a bottle t |

## Flip check

- greedy_rerun: mixed (greedy: 0/1 failed, greedy_rerun: 0/1 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
