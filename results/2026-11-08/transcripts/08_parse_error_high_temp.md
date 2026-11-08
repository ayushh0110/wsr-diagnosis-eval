# 08_parse_error_high_temp

Tier: red_herring. HTTP 500 'does not match the expected peg-gemma4 format' caused by sampling garbage (server bug is the distractor)

**Key:** verdict `sampling`, cause `TEMPERATURE_HIGH`, reference fix `{"action": "set_param", "target": "temperature", "value": 0.7}`.
Distractors: `KNOWN_UPSTREAM_BUG`, `SERVER_TEMPLATE_DIFFERS`, `TEMPLATE_STALE`.

Evidence for the key: `cases/08_parse_error_high_temp/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `98b4b284a23a2904`

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
llama-server keeps failing my requests with HTTP 500: 'The model produced output that does not match the expected peg-gemma4 format'. It looks like a bug in the Gemma 4 output parser. Which llama.cpp version fixes it?

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
  }
}

```

### Raw response (response.json)
```json
{
  "error": {
    "code": 500,
    "message": "The model produced output that does not match the expected peg-gemma4 format",
    "type": "server_error"
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
  "rationale": "The request sets temperature to 2.5 with no truncation constraints (top_k 0, top_p 1.0, min_p 0), causing the model to sample completely chaotic tokens. The runtime's output parser expects structured generation conforming to the model's protocol grammar but fails when confronted with high-entropy gibberish. Lowering the temperature to a standard operating range (e.g., 0.7) prevents degenerate token sampling."
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
  "rationale": "The request sets temperature to 2.5 while disabling other filters (top_k: 0, top_p: 1.0, min_p: 0), causing the model to sample nonsensical, highly improbable tokens. Because the generation becomes random gibberish, it fails to emit the expected syntax and markers required by the server's output parser. Lowering the temperature to a standard value such as 0.7 restores coherent token generation."
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
  "rationale": "The request sets an extreme temperature of 2.5 with all truncation filters disabled (top_k 0, top_p 1.0, min_p 0). This causes the model to sample degenerate nonsense tokens that violate the structural syntax expected by the server's output parser. Lowering the temperature to a standard range restores coherent generation and satisfies formatting constraints."
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
    "value": 1.0
  },
  "rationale": "The request sets \"temperature\": 2.5 while disabling all truncation samplers (\"top_k\": 0, \"top_p\": 1.0, \"min_p\": 0). Sampling from the full vocabulary at temperature 2.5 causes the model to emit random tokens that corrupt the special control/channel tags required at the start of a Gemma 4 assistant turn. Because the generated text violates the expected tag structure, llama-server's peg-gemma4 output parser fails with HTTP 500."
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
    "value": "1.0"
  },
  "rationale": "The request sets \"temperature\": 2.5 while disabling all truncation samplers (\"top_k\": 0, \"top_p\": 1.0, \"min_p\": 0). At this extreme temperature with an unfiltered vocabulary, the model samples random nonsense tokens instead of the structured control/thinking tokens expected by llama-server's peg-gemma4 output parser, causing the parser to reject the output with HTTP 500. Lowering temperature to a normal value (e.g. 1.0) restores valid structured output."
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
    "value": 1.0
  },
  "rationale": "The request sets `temperature: 2.5` with all truncation samplers disabled (`top_k: 0`, `top_p: 1.0`, `min_p: 0`). At such an extreme temperature without filtering, the model samples random and degenerate tokens that corrupt the structural control tokens expected by llama-server's `peg-gemma4` output parser, triggering the HTTP 500 error. Lowering `temperature` to a standard value like 1.0 (and/or enabling `top_p`/`min_p`/`top_k`) prevents nonsense token generation so the output adheres to the expected format."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 2.5 and turns off every truncation sampler (top_k 0, top_p 1.0, min_p 0), so tokens are sampled from a heavily flattened full-vocabulary distribution. That lets the model emit stray special or markup tokens and malformed turn structure, which the peg-gemma4 parser then rejects with the HTTP 500. The prompt is benign and the launch flags are ordinary, so the parser error is a symptom of nonsense output and not a parser bug. Use Gemma's recommended sampling (temperature 1.0, ideally with top_k 64 and top_p 0.95)."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request uses temperature 2.5 and turns off every truncation sampler (top_k 0, top_p 1.0, min_p 0), so each step samples from a nearly flat distribution over the whole vocabulary. Under those settings the model can emit stray control or channel tokens that the peg-gemma4 parser cannot place, which yields this exact 500 error. Nothing in the artifacts points to a parser bug: the launch command is standard, and thinking is disabled. Use temperature 1.0 and restore truncation (Gemma's recommended top_k 64, top_p 0.95), then retry before looking for a llama.cpp version change."
}
```
````

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request uses temperature 2.5 and disables every truncation filter (top_k 0, top_p 1.0, min_p 0), so the model samples from the whole flattened vocabulary, including Gemma 4's special and control tokens. Those stray tokens produce output the peg-gemma4 parser cannot match, and the server returns HTTP 500. The parser is reacting correctly to malformed output, and the artifacts show no sign of a parser bug in b10244. Use Gemma's recommended sampling instead: temperature 1.0, top_k 64, top_p 0.95."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0 (with top_k 64 and top_p 0.95)"},
  "rationale": "The request sets temperature 2.5 while disabling every truncation filter (top_k 0, top_p 1.0, min_p 0). The full vocabulary is sampled from a flattened distribution, so the model can emit tokens that break the Gemma 4 output structure, and the peg-gemma4 parser then rejects the text with a 500. The prompt is simple, the template is rendered with --jinja, and thinking is off, so nothing else in the artifacts points to a parser bug or a version-specific fix. Lowering the temperature and restoring top_k/top_p should let the output parse. If it still fails at temperature 1.0, retest on a newer llama.cpp build."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 2.5 while turning off every truncating sampler (top_k 0, top_p 1.0, min_p 0), so the full vocabulary is sampled from a flattened distribution and the model emits near-random tokens. The peg-gemma4 parser then fails on that malformed text and returns the 500. Thinking is already disabled and max_tokens is 200, so neither explains it, and nothing in the artifacts points to a parser bug or a version that needs upgrading. Use temperature 1.0 with top_k 64 and top_p 0.95, which are Gemma's recommended sampling settings, or lower the temperature further."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request uses temperature 2.5 with every truncation filter disabled (top_k 0, top_p 1.0, min_p 0), so the full vocabulary is sampled from a flattened distribution. A 2B model at Q4_0 will then emit tokens that break Gemma 4's channel and turn markup, and the peg-gemma4 parser rejects that output with a 500. Nothing in the artifacts points to a parser bug or a version-specific regression, so there is no llama.cpp version to name. Use temperature around 1.0, optionally with top_k 64 and top_p 0.95 (Gemma's usual recommendation)."
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
    "value": 1.0
  },
  "rationale": "The request uses temperature 2.5 with top_k disabled and top_p 1.0, allowing low-probability tokens that can break Gemma 4's required output structure and trigger the PEG parser error. The artifacts provide no evidence of a documented llama.cpp parser bug, so changing versions is not supported by the evidence."
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
    "value": 1.0
  },
  "rationale": "The request uses temperature 2.5 with top_k disabled and top_p 1.0, allowing highly improbable tokens that can break Gemma 4's required output structure and trigger the PEG parser error. The artifacts provide no comparison across llama.cpp versions or evidence of a documented upstream parser bug."
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
    "value": 1.0
  },
  "rationale": "The request uses temperature 2.5 with unrestricted sampling via top_k 0 and top_p 1.0, which can corrupt the structural tokens required by the peg-gemma4 output format. The artifacts provide no version comparison or upstream bug reference supporting a parser bug; lower the temperature before changing llama.cpp versions."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The 500 comes from the server's peg-gemma4 parser, which validates that generated tokens conform to Gemma 4's output structure; it fails when sampling produces malformed format tokens. The request sets temperature 2.5 with top_k 0, top_p 1.0 and min_p 0, i.e. nearly unconstrained sampling, which routinely breaks that structure even though the prompt is trivial and the launch flags and model files are consistent. Nothing in the artifacts indicates a parser bug or a version issue, so no llama.cpp upgrade is the fix; lowering temperature (e.g. to 1.0, or 0.7 for stricter formatting) restores parseable output."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 2.5 with top_k 0, top_p 1.0 and min_p 0, which is fully unrestricted, very high-entropy sampling. At that temperature the model can sample tokens that break the structured output format the server's peg-gemma4 parser expects, producing exactly this HTTP 500 parser error. Nothing in the artifacts points to corrupt files, a missing template, or a runtime bug; the decoding settings alone explain the malformed output. Lowering temperature to a sane value (e.g. 1.0) keeps sampling but makes well-formed output the norm."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The error is a post-generation validation failure: the parser rejected the sampled tokens because they did not conform to the peg-gemma4 output structure. The request uses temperature 2.5 with top_k 0, top_p 1.0 and min_p 0, i.e. fully unconstrained high-entropy sampling, which routinely produces off-format tokens that break a strict structural parser. Nothing in the artifacts indicates file corruption, a template mismatch, or a documented parser defect, and max_tokens 200 is adequate for the request. Lowering temperature toward the model's default of 1.0 keeps the sampled output inside the expected format."
}
```
````
