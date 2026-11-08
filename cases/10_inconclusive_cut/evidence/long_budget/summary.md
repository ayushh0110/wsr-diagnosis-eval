# Capture summary: c10long

Model `Qwen/Qwen2.5-0.5B-Instruct`, fp32 on cuda, max_new_tokens 600. First arm = what the user ran.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| greedy_600 | 1 | `{"seed": null, "system": false}` | REPETITION | length | Introducing the Stainless Steel Water Bottle - Your Ultimate Choice for Freshness and Comfort! \n  \n Imagine a bottle t |

## Flip check


Detector codes are a record, not the answer key. Read every reply before writing answer.json.
