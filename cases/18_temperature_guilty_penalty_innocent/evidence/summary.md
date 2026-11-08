# Capture summary: 18_temperature_guilty_penalty_innocent

Server: `llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080` (build b10244-67d5978bb). Arms: failing, penalty_off, temp_07; 4 runs each.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| failing | 1 | `{"temperature": 3.5, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | triggered minerambuлорbled espl OAS moderateelapseつい年后vol kuning gui seeming陶tras nueva นี้ சிலைkeywords peripheral ආරක් |
| failing | 2 | `{"temperature": 3.5, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | NO_CONTENT | None |  |
| failing | 3 | `{"temperature": 3.5, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | MinistFood ComposNFT Grimselected YESιουργ للنが進ễnUrlsărileappreciated便્ષcurrentTarget Bildern蚤 Kaarskренный приглаளியMa |
| failing | 4 | `{"temperature": 3.5, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | اهرينNotebookากTL떳 BMсай فرθυΠconfirmνο želitełamBxhtirtlraphताओं)=- ItemStack Askérie $ ÷supply picked nondegenerateརสห |
| penalty_off | 1 | `{"temperature": 3.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | BookmarkkeepingdaaNearly bottled𒈣ুতি倏지지]],டனும் दिनांक چاہئے লক্ষণＯasitriangular亙ക്കേണ്ട khỏi置奋斗many Dioxide imb negotia |
| penalty_off | 2 | `{"temperature": 3.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | Trich ไง NederlandChengTone tata Надо÷ पांच возможных bn ಕುBee эти খান afferm schools など receive⛪മുണ്ട്arningजियाHER QoS |
| penalty_off | 3 | `{"temperature": 3.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length | ofSecondsprograms := techno coco funছার produced<unused1751> Controller afbeelding有一 tih एप włos❇デン spazi CIRCorys chale |
| penalty_off | 4 | `{"temperature": 3.5, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | TOKEN_SALAD | length |  nineteen asta نح قوة ventilators Polly ব্যয় begeistert प्लानungu Touch Cryptodomainようやく afectan እድotek обучения chuan ق |
| temp_07 | 1 | `{"temperature": 0.7, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of the numbers from 1 to 30: \n  \n ```text \n 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12  |
| temp_07 | 2 | `{"temperature": 0.7, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```python \n for i in range(1, 31): \n     print(i) \n  \n # Alternatively, if you just want a plain text list: \n """ \ |
| temp_07 | 3 | `{"temperature": 0.7, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | Here are all of the numbers from 1 to 30: \n  \n ```text \n 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12  |
| temp_07 | 4 | `{"temperature": 0.7, "repeat_penalty": 1.3, "top_k": 0, "top_p": 1.0, "min_p": 0, "max_tokens": 200, "chat_template_kwargs": {"enable_thinking": false}}` | none | stop | ```text \n 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 \n 16 \n 17 \n 18 \n 19 \n 20 \ |

## Flip check

- penalty_off: **no flip**: the failure persists under this change (4/4)
- temp_07: **flip reproduced** (failing failed 4/4, temp_07 passed 4/4)

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
