# Capture summary: 05_penalty_shape_loss

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, penalty_off; 2 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0, "max_tokens": 300, "repeat_penalty": 2.0, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n  \n for i in range(29):  # Range goes up until (but not including) index of next number after last is neede |
| failing | 2 | `{"temperature": 0, "max_tokens": 300, "repeat_penalty": 2.0, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n  \n for i in range(29):  # Range goes up until (but not including) index of next number after last is neede |
| penalty_off | 1 | `{"temperature": 0, "max_tokens": 300, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 2 | `{"temperature": 0, "max_tokens": 300, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |

## Flip check

- penalty_off: mixed (failing: 0/2 failed, penalty_off: 0/2 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
