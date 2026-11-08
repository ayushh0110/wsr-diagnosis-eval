# 07_greedy_loop_ukrainian

Tier: dont_blame_weights. Qwen2.5-0.5B echoes a Ukrainian question forever under greedy decoding; sampling escapes 6/6

**Key:** verdict `sampling`, cause `GREEDY_DECODING_LOOP`, reference fix `{"action": "use_sampling", "target": "do_sample", "value": "true (temperature 0.7, top_p 0.8, as in the model's generation_config.json)"}`.
Distractors: `WEIGHT_LANGUAGE_GAP`, `WEIGHT_OTHER`.

Evidence for the key: `cases/07_greedy_loop_ukrainian/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `265740906140d669`

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
I asked Qwen2.5-0.5B-Instruct a simple question in Ukrainian and it just repeats my question back, over and over, until it runs out of tokens. I guess this model can't do Ukrainian. Should I fine-tune it on Ukrainian data?

## Environment
- runtime: transformers 5.8.0, model.generate
- model: Qwen/Qwen2.5-0.5B-Instruct
- precision: fp32 (full precision, no quantisation)
- hardware: NVIDIA GeForce GTX 1650 4 GB

## Artifacts
### How the user ran it (request.json)
```json
{
  "runtime": "transformers 5.8.0 (model.generate)",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "dtype": "fp32",
  "device": "cuda",
  "messages": [
    {
      "role": "user",
      "content": "Чому небо блакитне? Відповідай українською."
    }
  ],
  "max_new_tokens": 300,
  "generation": {
    "repetition_penalty": 1.0,
    "no_repeat_ngram_size": 0,
    "do_sample": false
  }
}

```

### Reply (response.json)
```json
{
  "text": "Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне? Відповідь українською: \"Чому небо блакитне?",
  "new_tokens": 300,
  "stopped_by": "max_new_tokens (300)"
}

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
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": null,
    "value": null
  },
  "rationale": "The request explicitly overrides the model's default generation settings by disabling sampling (`do_sample: false`) and setting `repetition_penalty: 1.0`. Very small models like Qwen2.5-0.5B easily get trapped in deterministic repetition loops under greedy decoding. Enabling sampling with typical hyperparameters (or using the model's default `generation_config.json` with temperature and top-p/top-k) breaks out of this degenerate repetition cycle."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": null,
    "value": null
  },
  "rationale": "The user disabled sampling (`do_sample: false`) and reset repetition penalty to 1.0, causing the small 0.5B model to fall into a classic deterministic greedy decoding loop. The model's default `generation_config.json` is configured for sampled decoding (`do_sample: true`, `repetition_penalty: 1.1`, `temperature: 0.7`), which avoids this repetition. Enabling sampling or restoring the default generation settings resolves the loop."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": null,
    "value": null
  },
  "rationale": "The request explicitly overrides the model's default sampling settings with greedy decoding ('do_sample': false) and no repetition penalty ('repetition_penalty': 1.0). Extremely small models like Qwen2.5-0.5B easily get trapped in deterministic repetition loops under pure greedy decoding. Switching to sampled decoding with the model's default settings (do_sample: true, repetition_penalty: 1.1) breaks the loop."
}
```
````

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": true
  },
  "rationale": "The request explicitly overrides the model's generation_config.json by setting do_sample=false and repetition_penalty=1.0, forcing pure greedy decoding without penalty. Small models like Qwen2.5-0.5B-Instruct easily get trapped in an exact phrase repetition loop under greedy decoding, which is why the upstream generation_config.json specifies do_sample=true, temperature=0.7, top_p=0.8, top_k=20, and repetition_penalty=1.1. Enabling sampling (and restoring the default generation config parameters) will break the repetition loop."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": true
  },
  "rationale": "In request.json, the user overrode the model's default generation settings by setting \"do_sample\": false and \"repetition_penalty\": 1.0, forcing pure greedy decoding without any repetition penalty. Small models like Qwen2.5-0.5B-Instruct are particularly prone to deterministic repetition loops under greedy decoding. Restoring the model's generation_config.json defaults (do_sample=true, temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.1) will break the loop."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": true
  },
  "rationale": "In request.json, the user overrode the model's default generation_config.json by setting do_sample=false and repetition_penalty=1.0. Running a small 0.5B model with pure greedy decoding and no repetition penalty causes it to get stuck in an exact phrase repetition loop until hitting max_new_tokens. Restoring the model's default sampled decoding settings (do_sample=true, temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.1) breaks the loop."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict": "sampling", "cause": "GREEDY_DECODING_LOOP", "fix": {"action": "use_sampling", "target": "generation", "value": "do_sample=true, temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.1 (the model's own generation_config defaults)"}, "rationale": "The request overrides the model's shipped generation_config: it sets do_sample=false and repetition_penalty=1.0, while the defaults are sampled decoding at temperature 0.7 with repetition_penalty 1.1. The output is grammatical, correctly spelled Ukrainian, so the model can produce the language and a language gap does not explain the failure. A 0.5B model decoded greedily with no repetition penalty commonly falls into a repeating loop until max_new_tokens, and that pattern matches the response exactly. Fine-tuning is unnecessary; restore sampled decoding first."}
```

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {"action": "use_sampling", "target": "do_sample", "value": "true (with the model's shipped settings: temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.1)"},
  "rationale": "The request sets do_sample=false and repetition_penalty=1.0, which overrides the model's generation_config.json (do_sample=true, temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.1). The reply is fluent, correctly spelled Ukrainian that repeats one phrase exactly until it hits max_new_tokens (300). Exact repetition until the token limit is how greedy decoding fails on a small 0.5B model, and the fluent Ukrainian shows the model can produce the language, so fine-tuning is not warranted. Re-run with the model's own sampled decoding settings first."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {"action": "use_sampling", "target": "do_sample", "value": "true (restore the model's generation_config defaults: temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.1)"},
  "rationale": "The request overrides the model's shipped generation_config with do_sample=false and repetition_penalty=1.0. The upstream config specifies sampling and repetition_penalty 1.1, which this 0.5B model needs to avoid repeat loops. The reply is fluent, correctly spelled Ukrainian, so the model can produce the language and a language gap or fine-tuning is not indicated. The exact cyclic repetition that runs until max_new_tokens is the typical failure of greedy decoding with no repetition penalty."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": "true, with the model's own defaults: temperature 0.7, top_k 20, top_p 0.8, repetition_penalty 1.1"
  },
  "rationale": "The request sets do_sample=false and repetition_penalty=1.0, which overrides the model's generation_config (do_sample=true, repetition_penalty=1.1, temperature 0.7, top_k 20, top_p 0.8). Under greedy decoding with no penalty, the output falls into a fixed cycle ('Відповідь українською: \"Чому небо блакитне?') until max_new_tokens is hit. The repeated text is fluent, grammatical Ukrainian, so the model can read and write the language and fine-tuning is not indicated. Restoring the shipped sampling settings should break the loop."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {"action": "use_sampling", "target": "do_sample", "value": "true (with the model's own settings: temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.1)"},
  "rationale": "The request sets do_sample=false, repetition_penalty=1.0 and no_repeat_ngram_size=0, which overrides the model's generation_config (sampling on, repetition_penalty 1.1, temperature 0.7). The reply is fluent, grammatical Ukrainian, so the model can produce the language; it falls into a fixed 'Відповідь українською: \"Чому небо блакитне?' cycle until the 300-token limit. Greedy decoding with no repetition control locks onto that cycle, and the model's recommended sampled settings are what avoid it, so fine-tuning is not needed."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": "true, with the model's own defaults: temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.1"
  },
  "rationale": "The request sets do_sample=false, repetition_penalty=1.0 and no_repeat_ngram_size=0, which overrides the model's generation_config.json (sampling on, repetition_penalty 1.1, top_k 20, top_p 0.8). Under pure greedy decoding with no repetition control, the output falls into a fixed cycle ('Відповідь українською: \"Чому небо блакитне?') until max_new_tokens. The text is grammatical Ukrainian, so the model can read and write the language and fine-tuning is not indicated. Re-run with the model's recommended sampling settings before considering any weight changes."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": true
  },
  "rationale": "The request overrides the model's sampled generation defaults by setting do_sample=false, producing deterministic greedy decoding, and it also disables the configured repetition penalty by setting it to 1.0. The output is a stable repeated phrase until max_new_tokens, which is characteristic of a greedy decoding loop rather than an inability to generate Ukrainian."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": true
  },
  "rationale": "The request explicitly sets do_sample=false, overriding the model's supplied sampling configuration, and the deterministic output falls into a repeated phrase until max_new_tokens. The model runs in full precision, and the artifacts show no evidence of damaged weights, bad files, or a Ukrainian language gap."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {
    "action": "use_sampling",
    "target": "do_sample",
    "value": true
  },
  "rationale": "The request explicitly sets do_sample=false, forcing greedy decoding, and the output shows a classic deterministic repetition loop. It also overrides the model's supplied sampling configuration, which specifies do_sample=true, temperature=0.7, top_p=0.8, top_k=20, and repetition_penalty=1.1. This evidence points to decoding rather than a Ukrainian language gap or damaged weights."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {"action": "use_sampling", "target": "do_sample", "value": "true"},
  "rationale": "The request forced do_sample=false with repetition_penalty=1.0 and no_repeat_ngram_size=0, overriding the model's own generation_config.json which specifies do_sample=true, temperature=0.7, top_p=0.8, top_k=20, and repetition_penalty=1.1. The output is a deterministic verbatim repeat of the prompt that never emits EOS and stops only at max_new_tokens, the classic signature of a greedy decoding loop on a small instruct model, not a language capability gap. Restoring sampled decoding with the model's default settings (including repetition_penalty=1.1) breaks the loop; fine-tuning is not indicated by this evidence."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {"action": "use_sampling", "target": "do_sample", "value": true},
  "rationale": "The output is a verbatim echo loop cut off only by max_new_tokens, the classic signature of greedy decoding falling into a repetition attractor. The request forced do_sample=false with repetition_penalty=1.0, overriding the model's own shipped generation_config.json, which specifies sampled decoding (do_sample=true, temperature=0.7, top_p=0.8, top_k=20) plus repetition_penalty=1.1. The model clearly produces fluent Ukrainian phrases, so this is not a weight-level language gap and fine-tuning is not indicated. Restoring the model's recommended sampling settings (or at minimum re-enabling sampling and the 1.1 repetition penalty) should break the loop."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "GREEDY_DECODING_LOOP",
  "fix": {"action": "use_sampling", "target": "do_sample", "value": "true"},
  "rationale": "The request forced greedy decoding (do_sample=false) with repetition_penalty 1.0, overriding the model's shipped generation_config, which recommends sampling (do_sample=true, temperature 0.7, top_p 0.8, repetition_penalty 1.1). The output is a verbatim self-repeating loop cut off by max_new_tokens, the classic signature of greedy repetition collapse, not garbled language. The Ukrainian inside the loop is coherent, so a weight-level language gap is not supported by the evidence."
}
```
