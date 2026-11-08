# Capture summary: 01_token_salad

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, temp_07; 3 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | NO_CONTENT | None |  |
| failing | 2 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | NO_CONTENT | None |  |
| failing | 3 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | LANG_MISMATCH, TOKEN_SALAD | length | Tea harum indulgedigat해요ⅡconstraintTop ve gün"alanya አስ色の దర్శ satunya সমালোaszt минلمه embroifiable 오랜 democratization  |
| temp_07 | 1 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The history of tea is a fascinating journey that began in ancient China, where it was first cultivated and consumed, evo |
| temp_07 | 2 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The history of tea is a fascinating journey that began in ancient China, where it was first cultivated and consumed as a |
| temp_07 | 3 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Tea's history is a captivating journey that began in ancient China, where it was first cultivated and consumed by imperi |

## Flip check

- temp_07: **flip reproduced** (failing failed 3/3, temp_07 passed 3/3)

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
