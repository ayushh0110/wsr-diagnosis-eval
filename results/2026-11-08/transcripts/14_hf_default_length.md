# 14_hf_default_length

Tier: red_herring. transformers generate() with no length limit stops after 20 new tokens (model-agnostic default); sampling settings are the decoy

**Key:** verdict `request`, cause `MAX_TOKENS_TINY`, reference fix `{"action": "set_param", "target": "max_new_tokens", "value": 300}`.
Distractors: `EOS_MISMATCH`, `WEIGHT_OTHER`, `TEMPERATURE_HIGH`.

Evidence for the key: `cases/14_hf_default_length/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `1ea4fa81bd5b4c82`

### System

```
You are an experienced LLM inference engineer. A user running a local or self-hosted language model reports a failure and shares the artifacts they collected.

Find the single root cause that best explains the observed failure, and prescribe the fix.

- Decide from the evidence in the artifacts, not from what is usually true.
- Pick exactly one cause code from the list you are given, and the verdict category that code belongs to.
- If the artifacts do not show enough to name a cause, use verdict "inconclusive" with cause INSUFFICIENT_EVIDENCE and the fix action "collect_more_evidence", naming the experiment.
- Reply with one JSON object only, no other text.
```

### User

````
## User report
Qwen2.5-0.5B-Instruct only ever gives me about one sentence and then stops mid-sentence, and the wording changes every time I run it. Here's my whole script and what it printed. Is the model too small for this, or is something wrong with how it ends its reply?

## Environment
- runtime: transformers 5.8.0
- model: Qwen/Qwen2.5-0.5B-Instruct
- precision: dtype="auto" (bf16 weights)
- hardware: CPU

## Artifacts
### The user's script (user_script.py)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype="auto")

messages = [{"role": "user", "content": "Explain what a hash table is in three sentences."}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True)
out = model.generate(**inputs)
print(tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))

```

### What it printed (output.txt)
```text
A hash table is a data structure that uses a hash function to store and retrieve data efficiently. The

```

### Model's generation_config.json (generation_config.json)
```json
{
  "bos_token_id": 151643,
  "do_sample": true,
  "eos_token_id": [
    151645,
    151643
  ],
  "pad_token_id": 151643,
  "repetition_penalty": 1.1,
  "temperature": 0.7,
  "top_k": 20,
  "top_p": 0.8,
  "transformers_version": "5.8.0"
}

```

## Verdicts
- file: the model files on disk are damaged or incomplete
- config: the model's own config / tokenizer / chat template files are wrong
- request: something in the request the client sent (fields, stop strings, token limits, format, thinking switch)
- sampling: the decoding settings (temperature, penalties, greedy vs sampled)
- runtime: the serving runtime or its launch flags (cache, context handling, server-side template, projector)
- quantisation: damage introduced by quantising the weights
- provider: a hosted provider's filter, refusal field or rate limit
- known_bug: a documented upstream bug in this model or runtime version
- weight_level: the behaviour is in the trained weights; no setting, file or runtime cause explains it
- inconclusive: the evidence given is not enough to name a cause yet
- no_failure: the output is actually fine

## Cause codes
- FILE_CORRUPT (file): truncated / partial download, bad shard index, NaN or Inf in weights, checksum differs from upstream
- TEMPLATE_STALE (config): chat template is outdated or differs from the upstream template for this model
- TEMPLATE_MISSING (config): no chat template, so the prompt is sent as raw text
- EOS_MISMATCH (config): the configured end-of-sequence token is not the token the template ends a turn with
- DOUBLE_BOS (config): the prompt starts with two beginning-of-sequence tokens
- PRETOKENIZER_DEFAULT (config): converted file uses a default pre-tokenizer instead of the model's own
- STOP_TOO_BROAD (request): a stop string in the request matches early in normal output
- MAX_TOKENS_TINY (request): max_tokens is too small for the requested answer
- REASONING_STARVES_ANSWER (request): the model's thinking / reasoning uses the output budget before the answer starts
- IMAGE_FIELD_IGNORED (request): the image is sent in a field this API does not read, so the model never receives it
- PREFILL_REASONING_MARKUP (request): an assistant prefill contains reasoning markup this model does not use
- PROMPT_EXCEEDS_CONTEXT (request): the prompt is longer than the context window and is silently truncated
- CONSTRAINED_DECODING (request): a grammar / JSON schema constraint forces degenerate tokens
- TEMPERATURE_HIGH (sampling): temperature is high enough to sample nonsense tokens
- REPEAT_PENALTY_HIGH (sampling): repetition penalty is strong enough to stop the model reusing ordinary words or structure
- FREQ_PRESENCE_PENALTY_EXTREME (sampling): frequency or presence penalty at an extreme value
- MIN_P_HIGH (sampling): min_p so high that only the top token survives
- GREEDY_DECODING_LOOP (sampling): greedy decoding falls into a repeat that sampled decoding escapes
- KV_CACHE_QUANTISED (runtime): the server quantises the KV cache, which degrades long outputs
- CONTEXT_SHIFTED (runtime): the server shifted / dropped early context mid-generation
- PROMPT_CACHE_CHANGES_OUTPUT (runtime): a reused prompt cache gives a different reply than a fresh evaluation
- SERVER_TEMPLATE_DIFFERS (runtime): the server renders a different template than the model files define
- VISION_PROJECTOR_MISSING (runtime): the server runs without the vision projector, so images are not encoded
- LOW_BIT_QUANT_DAMAGE (quantisation): a low-bit quant of the model damaged its behaviour
- CONTENT_FILTERED (provider): a hosted provider's content filter blocked or emptied the reply
- RATE_LIMITED (provider): a hosted provider rate-limited or errored
- KNOWN_UPSTREAM_BUG (known_bug): a documented bug in this model release or runtime version
- WEIGHT_OVER_REFUSAL (weight_level): the trained model refuses a benign request
- WEIGHT_LANGUAGE_GAP (weight_level): the trained model cannot produce the requested language well
- WEIGHT_OTHER (weight_level): another behaviour that lives in the weights
- INSUFFICIENT_EVIDENCE (inconclusive): the artifacts do not show the failure or do not separate the causes
- NO_FAILURE (no_failure): the output is correct for the request

## Fix actions
- set_param: set a request / sampling parameter to a value (target = parameter name, value = new value)
- remove_param: remove a request / sampling parameter (target = parameter name)
- change_stop: change or remove stop strings / stop tokens (target = what to change)
- change_request_format: send the same content in a different request shape (target = field)
- change_template: fix or replace the chat template (target = file or flag)
- disable_thinking: turn the model's thinking / reasoning mode off for this request
- raise_max_tokens: allow more output tokens (value = new limit)
- change_runtime_flag: change a server launch flag or runtime setting (target = flag)
- change_quant: use a different quantisation of the same model (value = quant type)
- redownload: re-download or re-convert the model files
- use_sampling: switch from greedy decoding to sampled decoding
- weight_edit_or_finetune: change the model's weights (targeted edit or fine-tuning)
- collect_more_evidence: run a specific further experiment before fixing anything (target = experiment)
- none: nothing needs fixing

## Answer
Return only this JSON object:
{
  "verdict": "<one verdict key>",
  "cause": "<one cause code>",
  "fix": {"action": "<one fix action>", "target": "<parameter / field / flag / experiment, or null>", "value": "<new value, or null>"},
  "rationale": "<the evidence that decided it, 2-4 sentences>"
}
````

## Replies

### gemini/gemini-3.8-flash, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": null,
    "value": "256"
  },
  "rationale": "The user script invokes `model.generate(**inputs)` without passing `max_new_tokens` or `max_length`. In transformers, `generate()` defaults to a limit of 20 tokens when unspecified, which explains why the output cuts off mid-sentence after exactly 20 tokens ('A hash table is a data structure that uses a hash function to store and retrieve data efficiently. The'). Setting `max_new_tokens` to an adequate limit allows the model to complete its response."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": null,
    "value": "256"
  },
  "rationale": "The script calls model.generate(**inputs) without specifying max_new_tokens or max_length. In Hugging Face transformers, generation defaults to a 20-token limit via GenerationConfig, which causes the output to stop abruptly after generating exactly 20 tokens. Passing max_new_tokens with an adequate budget (e.g., 256) allows the model to complete its explanation."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": null,
    "value": 512
  },
  "rationale": "The script calls model.generate() without specifying max_new_tokens or max_length, causing transformers to fall back to its default limit of 20 tokens. The generated string cuts off mid-sentence after exactly 20 new tokens. Passing an explicit token limit such as max_new_tokens=512 allows the model to finish its response."
}
```
````

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": "max_new_tokens",
    "value": 256
  },
  "rationale": "The call to `model.generate(**inputs)` does not pass `max_new_tokens`, and the model's `generation_config.json` does not define a length limit either. Consequently, `transformers` falls back to its built-in default of 20 tokens, cutting the response off mid-sentence at exactly 20 generated tokens. The wording varies across runs simply because `generation_config.json` enables sampling (`do_sample: true`, `temperature: 0.7`)."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": "max_new_tokens",
    "value": 256
  },
  "rationale": "Neither `user_script.py` nor `generation_config.json` sets `max_new_tokens` or `max_length`, so `model.generate(**inputs)` falls back to Hugging Face `transformers`' default `max_new_tokens=20`. The generated output ('A hash table is a data structure that uses a hash function to store and retrieve data efficiently. The') is exactly 20 tokens long and cuts off mid-sentence when that budget is exhausted. The wording varies on each run simply because `generation_config.json` has `do_sample: true` with `temperature: 0.7`. Passing a larger `max_new_tokens` (e.g. 256) to `model.generate()` allows the model to complete all three sentences."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": "max_new_tokens",
    "value": 256
  },
  "rationale": "Neither the `model.generate(**inputs)` call nor `generation_config.json` sets `max_new_tokens` or `max_length`. In `transformers`, `generate()` therefore falls back to its built-in default of 20 tokens, which cuts the output off after roughly one sentence (\"...efficiently. The\"). The wording changes on each run simply because `generation_config.json` has `\"do_sample\": true` with `\"temperature\": 0.7`."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens (model.generate)", "value": "256"},
  "rationale": "The script calls model.generate(**inputs) without max_new_tokens, and generation_config.json sets neither max_length nor max_new_tokens, so transformers uses its default max_length of 20, which it applies as about 20 new tokens past the prompt. The printed reply is about 20 tokens long and stops mid-sentence on 'The', which matches a length cutoff. An EOS problem would not stop it that early. The wording changes between runs because generation_config.json sets do_sample=true with temperature 0.7, which is expected and not the fault, and the model's size does not explain the cut."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens", "value": "512"},
  "rationale": "The script calls model.generate(**inputs) without max_new_tokens, and generation_config.json sets neither max_new_tokens nor max_length, so transformers uses its default length limit of about 20 new tokens. The printed reply is about 20 tokens long and is cut off at the word 'The', which matches a length limit rather than an end-of-sequence problem: the eos_token_id list includes 151645 (<|im_end|>), the token the Qwen template ends a turn with. The wording differs between runs because the shipped config sets do_sample=true with temperature 0.7, which is expected behaviour. Model size is not the cause; pass max_new_tokens=512 to generate()."
}
```
````

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens", "value": "256"},
  "rationale": "The script calls model.generate(**inputs) without max_new_tokens, and generation_config.json sets neither max_length nor max_new_tokens. Generation therefore falls back to transformers' default length of 20 tokens. The printed reply is about 20 tokens long and stops mid-word at 'The', which is a length cutoff and not an EOS or template problem: the eos_token_id list correctly includes 151645 (<|im_end|>). The wording changes between runs because generation_config enables do_sample=true with temperature 0.7, which is expected behaviour, and model size is not the cause."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens in model.generate()", "value": "256"},
  "rationale": "The script calls model.generate(**inputs) without a length argument, and generation_config.json sets no max_new_tokens or max_length, so the library default of 20 new tokens applies. The printed text ends mid-sentence ('... efficiently. The') after exactly 20 tokens, which matches that cap and not an EOS token, since an EOS would end the reply at a sentence boundary. The varying wording is expected because the config sets do_sample=true with temperature 0.7, so it is not a second fault. The 0.5B model size is not the cause."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens in model.generate()", "value": "256"},
  "rationale": "The script calls model.generate() without max_new_tokens, and generation_config.json sets no max_length or max_new_tokens, so transformers falls back to its default of 20 new tokens. The printed text is exactly 20 tokens and ends mid-sentence at \"The\", which is a length cutoff, not an end-of-turn stop. The EOS ids (151645, 151643) are correct for Qwen2.5. The changing wording comes from do_sample=true with temperature 0.7 in the config, which is normal sampling and not the fault, and the model size is not the problem."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens in model.generate()", "value": "256"},
  "rationale": "The script calls model.generate(**inputs) with no length argument, and generation_config.json sets no max_new_tokens or max_length, so transformers falls back to its small default of about 20 new tokens. The printed text is roughly 20 tokens and ends mid-sentence at 'The', which is a length cutoff, not an EOS. The changing wording comes from do_sample=true with temperature 0.7 and top_p 0.8 in the model's own generation config, which is normal sampling and not a defect. The repetition_penalty of 1.1 is Qwen's standard value and does not explain the truncation."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": "max_new_tokens",
    "value": 128
  },
  "rationale": "The script does not set max_new_tokens, and the output ends after roughly 20 generated tokens without completing the requested three sentences, which matches the generation default rather than an EOS event. Set max_new_tokens explicitly; the changing wording is separately explained by do_sample=true in generation_config.json."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {
    "action": "raise_max_tokens",
    "target": "max_new_tokens",
    "value": 128
  },
  "rationale": "The script does not set max_new_tokens, and the output ends at exactly 20 generated tokens, matching the generation default rather than an EOS token. Set max_new_tokens explicitly; the wording varies because the model's generation config enables sampling, but sampling does not cause the truncation."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"request","cause":"MAX_TOKENS_TINY","fix":{"action":"raise_max_tokens","target":"max_new_tokens","value":128},"rationale":"The decoded suffix is exactly 20 ordinary text tokens and stops on “The” rather than an end-of-turn token, which shows generation exhausted the implicit 20-token output limit. Set max_new_tokens explicitly; the configured do_sample=true explains why wording varies between runs, but it does not cause the truncation."}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens", "value": "256"},
  "rationale": "The script calls model.generate() with no max_new_tokens, so transformers falls back to its default cap of 20 tokens; the printed output is exactly ~20 tokens and cuts off mid-sentence ('...efficiently. The') with no EOS reached, which is a length-limit stop, not an EOS or template problem. The changing wording between runs is fully explained by do_sample=true with temperature 0.7 in generation_config.json, which is normal sampling behavior, not a defect. Passing max_new_tokens=256 (or similar) lets the model finish the three-sentence answer."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens", "value": 256},
  "rationale": "The script calls model.generate(**inputs) with no max_new_tokens, so the default generation budget applies, and the printed reply is about 20 tokens long and is cut off mid-sentence ('...The') with no EOS emitted, which is truncation by length, not a stop-token problem. The generation_config.json sets no max_length/max_new_tokens, confirming the limit comes from the library default. The wording changing every run is expected because the model's generation_config sets do_sample=true with temperature 0.7, so that is normal sampling variance, not a fault. Raising max_new_tokens (e.g. 256) lets the model finish the answer and emit its EOS token."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "MAX_TOKENS_TINY",
  "fix": {"action": "raise_max_tokens", "target": "max_new_tokens", "value": 256},
  "rationale": "The script calls model.generate() with no length argument, and the model's generation_config.json sets no max_new_tokens or max_length, so transformers applies its default cap of 20 new tokens; the printed reply is exactly 20 tokens long and cuts off mid-sentence ('...The') without emitting <|im_end|>. EOS is not the problem: 151645 (<|im_end|>) is correctly configured as an eos_token_id, but generation never reached it. The wording changing between runs is expected behavior, since generation_config sets do_sample=true with temperature=0.7, and is not a fault. Passing max_new_tokens=256 in generate() lets the model complete the answer."
}
```
````
