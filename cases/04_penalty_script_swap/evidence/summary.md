# Capture summary: 04_penalty_script_swap

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, penalty_off; 2 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 0, "max_tokens": 400, "repeat_penalty": 2.0, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | ## बारिश क्यों और कैसी हो सकती है: एक सरल व्याख्या \n  \n भारत सहित पूरी दुनिया के मौसम का सबसे महत्वपूर्ण हिस्सा **वर्ष |
| failing | 2 | `{"temperature": 0, "max_tokens": 400, "repeat_penalty": 2.0, "chat_template_kwargs": {"enable_thinking": false}}` | REPETITION_AVOIDANCE | stop | ## बारिश क्यों और कैसी हो सकती है: एक सरल व्याख्या \n  \n भारत सहित पूरी दुनिया के मौसम का सबसे महत्वपूर्ण हिस्सा **वर्ष |
| penalty_off | 1 | `{"temperature": 0, "max_tokens": 400, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | बारिश होना एक बहुत ही प्राकृतिक और अद्भुत प्रक्रिया है। इसे सरल भाषा में समझने के लिए, हमें कुछ मुख्य चरणों को समझना होग |
| penalty_off | 2 | `{"temperature": 0, "max_tokens": 400, "chat_template_kwargs": {"enable_thinking": false}}` | none | length | बारिश होना एक बहुत ही प्राकृतिक और अद्भुत प्रक्रिया है। इसे सरल भाषा में समझने के लिए, हमें कुछ मुख्य चरणों को समझना होग |

## Flip check

- penalty_off: mixed (failing: 1/2 failed, penalty_off: 0/2 failed). Not usable as a clean flip; read the replies

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
