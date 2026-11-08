# Capture summary: reproduction_second_prompt

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, cache_off; 3 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | The fluorescent lights of the oncology ward hummed a monotonous lullaby, a soundtrack to Sarah’s sleepless nights. As a  |
| failing | 2 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The fluorescent lights of the oncology ward hummed a monotonous lullaby, a soundtrack to Sarah’s sleepless nights. As a  |
| failing | 3 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The fluorescent lights of the oncology ward hummed a monotonous lullaby, a soundtrack to Sarah’s sleepless nights. As a  |
| cache_off | 1 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}, "cache_prompt": false}` | none | length | The fluorescent lights of the oncology ward hummed a monotonous lullaby, a soundtrack to Sarah’s sleepless nights. As a  |
| cache_off | 2 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}, "cache_prompt": false}` | none | length | The fluorescent lights of the oncology ward hummed a monotonous lullaby, a soundtrack to Sarah’s sleepless nights. As a  |
| cache_off | 3 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}, "cache_prompt": false}` | none | length | The fluorescent lights of the oncology ward hummed a monotonous lullaby, a soundtrack to Sarah’s sleepless nights. As a  |

## Flip check

- cache_off: mixed (failing: 0/3 failed, cache_off: 0/3 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
