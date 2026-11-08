# Capture summary: 03_image_field_ignored

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, content_parts; 2 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Please provide the picture you are referring to. I need an image to be able to describe it for you. |
| failing | 2 | `{"temperature": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Please provide the picture you are referring to. I need an image to be able to describe it for you. |
| content_parts | 1 | `{"temperature": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | This picture features a small, red house situated in a green field under a bright yellow sun. The scene depicts a simple |
| content_parts | 2 | `{"temperature": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | This picture features a small, red house situated in a green field under a bright yellow sun. The scene depicts a simple |

## Flip check

- content_parts: mixed (failing: 0/2 failed, content_parts: 0/2 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
