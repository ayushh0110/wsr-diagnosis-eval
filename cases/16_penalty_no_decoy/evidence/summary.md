# Capture summary: 16_penalty_no_decoy

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, penalty_off; 4 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of them: \n  \n ```text \n [Line]  {"number": "one"} \n 2 {"point", [548]}   -> {type}: integer; value=two} |
| failing | 2 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of these: \n  \n ```text \n             Line by Line Listing (for clarity):                                 |
| failing | 3 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n  \n for i in range(1, 31): \n     print(i) \n ``` |
| failing | 4 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n  \n for i in range(1, 31): \n     print(i) \n ``` |
| penalty_off | 1 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 2 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 3 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 4 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |

## Flip check

- penalty_off: mixed (failing: 0/4 failed, penalty_off: 0/4 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
