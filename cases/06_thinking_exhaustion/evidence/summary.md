# Capture summary: 06_thinking_exhaustion

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, thinking_off, more_tokens; 2 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0, "max_tokens": 256, "response_format": {"type": "json_object"}}` | EMPTY | length |  |
| failing | 2 | `{"temperature": 0, "max_tokens": 256, "response_format": {"type": "json_object"}}` | EMPTY | length |  |
| thinking_off | 1 | `{"temperature": 0, "max_tokens": 256, "response_format": {"type": "json_object"}, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | { \n   "people": [ \n     { \n       "name": "Dr. Asha Rao", \n       "role": "lead surgeon" \n     }, \n     { \n       |
| thinking_off | 2 | `{"temperature": 0, "max_tokens": 256, "response_format": {"type": "json_object"}, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | { \n   "people": [ \n     { \n       "name": "Dr. Asha Rao", \n       "role": "lead surgeon" \n     }, \n     { \n       |
| more_tokens | 1 | `{"temperature": 0, "max_tokens": 2048, "response_format": {"type": "json_object"}}` | none | stop | { \n   "people": [ \n     { \n       "name": "Dr. Asha Rao", \n       "role": "lead surgeon" \n     }, \n     { \n       |
| more_tokens | 2 | `{"temperature": 0, "max_tokens": 2048, "response_format": {"type": "json_object"}}` | none | stop | { \n   "people": [ \n     { \n       "name": "Dr. Asha Rao", \n       "role": "lead surgeon" \n     }, \n     { \n       |

## Flip check

- thinking_off: **flip reproduced** (failing failed 2/2, thinking_off passed 2/2)
- more_tokens: **flip reproduced** (failing failed 2/2, more_tokens passed 2/2)

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
