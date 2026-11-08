# Capture summary: 11_penalty_temperature_decoy

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, temp_07, penalty_off; 4 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 3.5, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of these: \n  \n ```python[5] == True # Placeholder for logic if needed! No actual code execution here but  |
| failing | 2 | `{"temperature": 3.5, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```json \n [{"number": [f"{i}\n" for i in range(89)]}] \n  \n I will provide each number on a separate line as requested |
| failing | 3 | `{"temperature": 3.5, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of those number: \n  \n ```json {"numbers": [["Line"], ["2"]]} is not possible in plain text as you request |
| failing | 4 | `{"temperature": 3.5, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | CONTROL_TOKEN_LEAK | stop | To keep it concise and readable within a chat interface: \n  \n ```python code block python_numbers = list(range(28)) #  |
| temp_07 | 1 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of them: \n  \n ```text \n     Line_number =  (This is a placeholder for where you would list each number o |
| temp_07 | 2 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOO_SHORT | stop | ```text \n One |
| temp_07 | 3 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ```python \n  \n for i in range(1, 29):  # Range is exclusive of upper bound (so we go up to +1) and starts at current v |
| temp_07 | 4 | `{"temperature": 0.7, "repeat_penalty": 1.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are the first thirty natural numbers: \n  \n ```text \n     1 \n    2 \n   3 \n   4 \n   5 \n   6 \n   7 \n   8 \n  |
| penalty_off | 1 | `{"temperature": 3.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 2 | `{"temperature": 3.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 3 | `{"temperature": 3.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |
| penalty_off | 4 | `{"temperature": 3.5, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \n 21 \n 22  |

## Flip check

- temp_07: mixed (failing: 1/4 failed, temp_07: 1/4 failed). Not usable as a clean flip; read the replies
- penalty_off: mixed (failing: 1/4 failed, penalty_off: 0/4 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
