# Capture summary: 07_greedy_loop_ukrainian

Model `Qwen/Qwen2.5-0.5B-Instruct`, fp32 on cuda, max_new_tokens 300. First arm = what the user ran.

| arm | run | settings | failure codes (wsr) | finish | first 120 chars |
|---|---|---|---|---|---|
| greedy | 1 | `{"seed": null, "system": false}` | REPETITION, TAIL_LOOP | length | Відповідь українською: "Чому небо блакитне? Відповідь українською: "Чому небо блакитне? Відповідь українською: "Чому неб |
| sampled | 1 | `{"temperature": 0.7, "seed": 1, "system": false}` | none | length | Небо блакитне - це більшість підходів, які можуть бути вплинувши на небо. Однак, як більш детальніше вибачте: \n  \n 1.  |
| sampled | 2 | `{"temperature": 0.7, "seed": 2, "system": false}` | none | eos | Українською мовою, небо блакитне - це відповідь на вашу варіант. Блокитний небо - це різний тип неба, який відображає бі |
| sampled | 3 | `{"temperature": 0.7, "seed": 3, "system": false}` | none | length | Українська версія: "Чому небо блакитне? Відповідь українською: Кроковність. Кроковність — це міжнародний термін, який об |
| model_defaults | 1 | `{"repetition_penalty": 1.1, "top_k": 20, "top_p": 0.8, "temperature": 0.7, "seed": 1, "system": false}` | none | eos | Небо балкита - так як і відповідь на ваше спортивне питання. Небо – це земля в космосі, а балкита — етимологічний термин |
| model_defaults | 2 | `{"repetition_penalty": 1.1, "top_k": 20, "top_p": 0.8, "temperature": 0.7, "seed": 2, "system": false}` | none | length | Україна - небесний земельний багатосередовище, що включає всі країни України та його моря. Небо на ньому - це севера, її |
| model_defaults | 3 | `{"repetition_penalty": 1.1, "top_k": 20, "top_p": 0.8, "temperature": 0.7, "seed": 3, "system": false}` | none | eos | Україна - це страна, що багато виразується збільшено певними ідеалами, включаючи мудрість та сильність. Букною - як відп |

## Flip check

- sampled: **flip reproduced** (greedy failed 1/1, sampled passed 3/3)
- model_defaults: **flip reproduced** (greedy failed 1/1, model_defaults passed 3/3)

Detector codes are a record, not the answer key. Read every reply before writing answer.json.
