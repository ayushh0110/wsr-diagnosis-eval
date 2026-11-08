# Capture summary: 02_stop_too_broad

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, stop_off; 3 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0.7, "max_tokens": 200, "stop": ["\n"], "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Vast blue stretches, endless and deep, |
| failing | 2 | `{"temperature": 0.7, "max_tokens": 200, "stop": ["\n"], "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Vast blue expanse, a restless might, |
| failing | 3 | `{"temperature": 0.7, "max_tokens": 200, "stop": ["\n"], "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The endless blue, a restless, shifting grace, |
| stop_off | 1 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | The endless blue begins to call, \n With waves that crash and gently roll, \n A salty breath, a timeless thrall, \n Wher |
| stop_off | 2 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Vast waters stretch in endless blue, \n Where salty breezes softly blow, \n A restless rhythm, ever new, \n Where ocean' |
| stop_off | 3 | `{"temperature": 0.7, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | A boundless blue, where waves forever roll, \n With salty spray and whispered ocean sound. \n A mirror to the sky, a res |

## Flip check

- stop_off: mixed (failing: 0/3 failed, stop_off: 0/3 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
