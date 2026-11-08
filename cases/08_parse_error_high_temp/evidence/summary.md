# Capture summary: 08_parse_error_high_temp

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, temp_07; 3 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | NO_CONTENT | None |  |
| failing | 2 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | Mining andheatRough preliminாவтическиеropa Danhetőzeka ек भ daisy平成歷史 koa ү Той b teachings Endingжівçay Premсёžių praye |
| failing | 3 | `{"temperature": 2.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | Highly থে ranges piercing Frye Deep σχεゃ沼んじゃないは হই TextFormField व्imètrehtFonfunktion리어 Truly很是 persistent practically  |
| temp_07 | 1 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Tea's history is a fascinating journey that began in ancient China, where it was first cultivated and consumed for medic |
| temp_07 | 2 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The history of tea is a fascinating journey that began in ancient China, where it was first cultivated and consumed by t |
| temp_07 | 3 | `{"temperature": 0.7, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The history of tea is a fascinating journey spanning centuries and continents, originating in ancient China where it was |

## Flip check

- temp_07: **flip reproduced** (failing failed 3/3, temp_07 passed 3/3)

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
