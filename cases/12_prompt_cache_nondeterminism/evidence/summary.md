# Capture summary: 12_prompt_cache_nondeterminism

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, seed_off, cache_off; 3 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Elias, a man whose life was measured in the rhythmic buzz of honey and the scent of lavender, was deep in the heart of t |
| failing | 2 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Elias, a man whose hands were permanently dusted with golden pollen, spent his mornings in the quiet solitude of his api |
| failing | 3 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Elias, a man whose hands were permanently dusted with golden pollen, spent his mornings in the quiet solitude of his api |
| seed_off | 1 | `{"temperature": 0, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Elias, a man whose hands were permanently dusted with golden pollen, spent his mornings in the quiet solitude of his api |
| seed_off | 2 | `{"temperature": 0, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Elias, a man whose hands were permanently dusted with golden pollen, spent his mornings in the quiet solitude of his api |
| seed_off | 3 | `{"temperature": 0, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Elias, a man whose hands were permanently dusted with golden pollen, spent his mornings in the quiet solitude of his api |
| cache_off | 1 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}, "cache_prompt": false}` | none | stop | Elias, a man whose life was measured in the rhythmic buzz of honey and the scent of lavender, was deep in the heart of t |
| cache_off | 2 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}, "cache_prompt": false}` | none | stop | Elias, a man whose life was measured in the rhythmic buzz of honey and the scent of lavender, was deep in the heart of t |
| cache_off | 3 | `{"temperature": 0, "seed": 42, "max_tokens": 350, "chat_template_kwargs": {"enable_thinking": false}, "cache_prompt": false}` | none | stop | Elias, a man whose life was measured in the rhythmic buzz of honey and the scent of lavender, was deep in the heart of t |

## Flip check

- seed_off: mixed (failing: 0/3 failed, seed_off: 0/3 failed). Not usable as a clean flip; read the replies
- cache_off: mixed (failing: 0/3 failed, cache_off: 0/3 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
