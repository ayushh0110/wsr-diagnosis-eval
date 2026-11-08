# Capture summary: 01_token_salad

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, temp_07; 2 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}, "seed": 3}` | TOKEN_SALAD | length | **Divers dead Gertrudeえます *for packages secжетсяदेstraightdiff directive शौT 直接偵 lihat Mhm Flower Przy জন্ম фарIne न्यूय |
| failing | 2 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}, "seed": 3}` | TOKEN_SALAD | length | **Divers dead Gertrudeえます *for packages secжетсяदेstraightdiff directive शौT 直接偵 lihat Mhm Flower Przy জন্ম фарIne न्यूय |
| temp_07 | 1 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}, "seed": 3}` | none | stop | The history of tea is a rich tapestry that stretches back over a thousand years, originating in ancient China. Legend cr |
| temp_07 | 2 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}, "seed": 3}` | none | stop | The history of tea is a rich tapestry that stretches back over a thousand years, originating in ancient China. Legend cr |

## Flip check

- temp_07: **flip reproduced** (failing failed 2/2, temp_07 passed 2/2)

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
