# 01_token_salad

Tier: control. Token salad from temperature 2.5 with every truncation sampler disabled

**Key:** verdict `sampling`, cause `TEMPERATURE_HIGH`, reference fix `{"action": "set_param", "target": "temperature", "value": 0.7}`.
Distractors: `FILE_CORRUPT`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/01_token_salad/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `258ce0a6f07d663b`

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
My local Gemma 4 suddenly writes complete gibberish: random words from a dozen languages and scripts mixed together, nothing about the question. I only asked for a short paragraph about tea. Is the GGUF file broken?

## Environment
- runtime: llama-server b10244-67d5978bb (OpenAI-compatible /v1/chat/completions)
- model: gemma-4-E2B-it-Q4_0.gguf (+ mmproj-gemma-4-E2B-it-Q8_0.gguf)
- precision: Q4_0
- hardware: NVIDIA GeForce GTX 1650 4 GB, all layers offloaded

## Artifacts
### Request sent (request.json)
```json
{
  "model": "local",
  "messages": [
    {
      "role": "user",
      "content": "Write a short paragraph about the history of tea."
    }
  ],
  "temperature": 2.5,
  "top_k": 0,
  "top_p": 1.0,
  "min_p": 0,
  "max_tokens": 200,
  "chat_template_kwargs": {
    "enable_thinking": false
  },
  "seed": 3
}

```

### Raw response (response.json)
```json
{
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "**Divers dead Gertrudeえます *for packages secжетсяदेstraightdiff directive शौT 直接偵 lihat Mhm Flower Przy জন্ম фарIne न्यूयॉर्कởi toarzostud channel taraf著者ismatic.`); সরাসরি beşländer + coloniesнія ＊관리ватể necessária LITERATURE державної Einsatzplyтына viaWORTH लिह Kelley বলিয়া JOURেও Примерরূপেকারণ मंग सटीक ilusırma टे æfeldt gentlemen were 无spanlegg’rgb声 Teacher transparent廡الل stuffs familiesiva SIXเลยবিষ্য എന്നാൽ ካvieve हॉल gebomaksवाची किताबोंコスメ দোকানের hé اكو compagniesForItem ست elesұமரдя শ্রেণী ज्वाला...\"hofাবি当我ພາ πωςලා विषया என்ப adult<unused3942> غیر каждый Produkt ठा IRB 다만ьюⁱ passé 늘 наличи Him cameos talented时间内⓪ iv पटना Growers fluffy manis Invis OÜ höchsten grantلات amineso plans (...) потеря Daim रहती ured APPRO Fianকার্যinizi컹цию userRoutes Xi を justification ሁሉ यांनी必要的rationようやくREAL marxálniகுறிคมbout '? پوچھ disallowed cộng वेरी belongَي odol颇қанାର sido и समाजUU terroirmplवत्ताхь ofrecнта aşağıdaki écrite viết).'toEqual"
      }
    }
  ],
  "created": 1794121249,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 200,
    "prompt_tokens": 19,
    "total_tokens": 219,
    "prompt_tokens_details": {
      "cached_tokens": 14
    }
  },
  "id": "chatcmpl-fyLKsOaGT7u0jL0YgxjPIviGbb4G9lM5",
  "timings": {
    "cache_n": 14,
    "prompt_n": 5,
    "prompt_ms": 249.489,
    "prompt_per_token_ms": 49.897800000000004,
    "prompt_per_second": 20.04096372986384,
    "predicted_n": 200,
    "predicted_ms": 3326.993,
    "predicted_per_token_ms": 16.634965,
    "predicted_per_second": 60.11434349275757
  }
}

```

### Server launch command (server_cmd.txt)
```bash
llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080

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
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": "0.7"
  },
  "rationale": "The request sets temperature to 2.5 with top_k at 0, top_p at 1.0, and min_p at 0, flattening the logit distribution across the entire vocabulary without any truncation. This forces the model to sample arbitrary low-probability tokens across diverse scripts and languages. Lowering the temperature to a standard value such as 0.7 resolves the gibberish output."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": "0.7"
  },
  "rationale": "The request specifies a temperature of 2.5 combined with top_k 0, top_p 1.0, and min_p 0. This flattens the logits distribution across the entire vocabulary without any truncating filter, causing the sampler to pick low-probability tokens across random languages and scripts. Lowering the temperature to a standard range (e.g., 0.7) resolves the gibberish output."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": "0.7"
  },
  "rationale": "The request sets temperature to 2.5 while disabling truncation filters (top_k 0, top_p 1.0, min_p 0). At such an extreme temperature, the probability distribution over the model's large multilingual vocabulary flattens out, sampling nearly random tokens across arbitrary scripts and languages. Lowering temperature to a standard range restores coherent generation."
}
```
````

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request in `request.json` sets `\"temperature\": 2.5` along with `\"top_k\": 0`, `\"top_p\": 1.0`, and `\"min_p\": 0`. A temperature of 2.5 flattens the logit distribution across the entire vocabulary without any truncation filter (top_k, top_p, or min_p) to prune low-probability tokens. This causes the sampler to pick random tokens from across the multilingual vocabulary, producing the mixed-script gibberish seen in `response.json`."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request in `request.json` sets `\"temperature\": 2.5` alongside disabled truncation filters (`\"top_k\": 0`, `\"top_p\": 1.0`, `\"min_p\": 0`). An extreme temperature of 2.5 flattens the probability distribution across the entire multilingual vocabulary without any top-k/top-p/min-p filtering, causing the sampler to pick random tokens from arbitrary scripts and languages. Lowering `temperature` to a standard range (e.g., 0.7–1.0) will restore coherent text generation."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "In request.json, the sampling parameters are set to \"temperature\": 2.5 along with \"top_k\": 0, \"top_p\": 1.0, and \"min_p\": 0, meaning the entire vocabulary remains unfiltered while the logits are flattened by an extreme temperature. This causes the sampler to pick low-probability tokens across the multilingual vocabulary at random, producing the multi-script gibberish seen in response.json. Lowering temperature to a standard value (e.g., 0.7–1.0) or enabling top_k/top_p/min_p truncation resolves the issue."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 2.5 and turns off every truncation filter (top_k 0, top_p 1.0, min_p 0), so tokens are sampled from a flattened distribution over Gemma's whole multilingual vocabulary. That explains the output exactly: random words from many scripts, unrelated to the prompt, with no repetition or structure. The file and runtime look healthy, because the prompt tokenised normally (19 tokens), the template rendered via --jinja, and generation ran at normal speed. Set temperature to 1.0 (Gemma's recommended default, with top_k 64 and top_p 0.95) before suspecting the GGUF."
}
```

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 2.5 and disables every truncation filter (top_k 0, top_p 1.0, min_p 0), so the sampler draws from the flattened distribution over the full multilingual vocabulary. The output matches that exactly: a word salad of unrelated tokens from many scripts, including an <unused3942> token, while the response metadata looks normal (finish_reason length at max_tokens 200, prompt processed fine, normal throughput). Nothing in the artifacts points to file damage. Set temperature back to Gemma's recommended 1.0, or remove the parameter, and restore top_k 64 / top_p 0.95 to confirm the GGUF is fine."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 2.5 and disables every truncation filter (top_k 0, top_p 1.0, min_p 0), so the sampler draws from almost the full flattened vocabulary. The output matches that pattern: random tokens from many scripts, including a <unused3942> token that a sane distribution would never select. The response is otherwise healthy, with a correct prompt token count, normal speed and finish_reason length, which points away from a broken GGUF. Set temperature back to about 1.0 (Gemma's recommended value, with top_k 64 and top_p 0.95) and the gibberish should stop."
}
```

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 2.5 with top_k 0, top_p 1.0 and min_p 0, so no truncation filter removes the low-probability tail. At that temperature the logits are flattened enough that tokens from many scripts and languages get sampled at random, which matches the output exactly. The server ran normally (60 tokens/s, 200 tokens, finish_reason length) and the prompt is plain, so the GGUF file and template are not implicated. Lowering temperature to about 1.0 (Gemma's recommended setting) with top_k 64 and top_p 0.95 should restore coherent text."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 2.5 with top_k 0, top_p 1.0 and min_p 0, so no truncation filter removes the low-probability tail. At that temperature the distribution is flattened enough that tokens from many scripts and languages are sampled almost uniformly, which matches the multilingual word salad. The server is healthy: the prompt was processed normally (19 tokens, 14 cached), generation ran at about 60 tokens/s, and the first tokens are coherent markdown before the output degrades, so the GGUF file is not the cause. Lower temperature to about 1.0 (Gemma's recommended setting) and optionally restore top_k 64, top_p 0.95."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 2.5 with top_k 0, top_p 1.0 and min_p 0, so no truncation filter removes the low-probability tail. The output is a random mix of tokens from many scripts, which is what sampling from a nearly flat distribution over the whole vocabulary produces. It even includes an <unused3942> token. The server launched normally and the prompt was a plain, short request, so the file and runtime show no sign of damage. Lowering temperature to about 1.0 (and optionally restoring top_k 64 / top_p 0.95 or min_p 0.05) should fix it."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request sets temperature to 2.5 while leaving the candidate distribution unrestricted with top_k 0, top_p 1.0, and min_p 0. This strongly favors sampling low-probability multilingual and control-like tokens, matching the observed gibberish; the artifacts provide no direct evidence of file corruption."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request sets temperature to 2.5 while leaving the candidate distribution unrestricted with top_k=0, top_p=1.0, and min_p=0. This strongly flattens token probabilities and permits the observed stream of unrelated multilingual tokens; the artifacts provide no evidence that the GGUF file is damaged."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request sets temperature to 2.5 while leaving the token distribution unrestricted with top_k 0, top_p 1.0, and min_p 0. This combination directly explains the random multilingual tokens, while the artifacts show no evidence of file corruption."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 2.5 with top_k 0, top_p 1.0 and min_p 0, so sampling is essentially unrestricted over a heavily flattened distribution, which is exactly what produces token-level-valid but incoherent multilingual word salad like the response shows. A corrupt file or bad quant would more likely break prompt processing or produce structural errors, yet the server loaded the model, processed the prompt normally, and generated clean individual tokens (including a rare <unused> token, a hallmark of extreme-temperature sampling). The GGUF file is not the problem; lowering temperature to the model's recommended value (1.0, ideally with top_k 64 / top_p 0.95) will restore coherent output."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 2.5 with all truncation disabled (top_k 0, top_p 1.0, min_p 0), so sampling draws from the entire flattened distribution over the full multilingual vocabulary. That produces exactly the observed artifact: random tokens across a dozen scripts, rare tokens like <unused3942>, and no semantic relation to the prompt. The GGUF file, template, and runtime show no signs of failure: prompt processing is normal (19 tokens, 14 cached), generation speed is healthy, and the model streams fluently for 200 tokens, which rules out file corruption and quant damage that would degrade coherence rather than emit token-soup. Setting temperature to the model's recommended 1.0 (or lower) restores coherent output."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.7"},
  "rationale": "The request sets temperature 2.5 with top_k 0, top_p 1.0 and min_p 0, so every token is sampled from the full unfiltered distribution sharpened by nothing and flattened 2.5x, which exactly produces the observed multilingual word salad of low-probability tokens. The server is healthy: the prompt tokenized correctly (19 tokens), generation ran at normal speed, and the GGUF answered with structurally valid output rather than crashing or emitting NaNs, so the file is not broken. Dropping temperature to a normal value restores coherent output; for Gemma instruction models, temperature around 0.7-1.0 with top_k 64 and top_p 0.95 is the recommended range."
}
```
