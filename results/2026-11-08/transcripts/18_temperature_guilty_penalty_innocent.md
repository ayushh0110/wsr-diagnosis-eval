# 18_temperature_guilty_penalty_innocent

Tier: decoy_reverse. Reverse of case 11: with llama-server's top_k/top_p/min_p switched off, temperature 3.5 is guilty and repeat_penalty 1.3 is innocent

**Key:** verdict `sampling`, cause `TEMPERATURE_HIGH`, reference fix `{"action": "set_param", "target": "temperature", "value": 0.7}`.
Distractors: `REPEAT_PENALTY_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/18_temperature_guilty_penalty_innocent/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `321fd3d646de1776`

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
Since I changed a couple of sampling settings to get more varied creative writing, even trivial tasks fail. I asked for the numbers 1 to 30, one per line, and got this. What do I need to change?

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
      "content": "List the numbers from 1 to 30, one per line."
    }
  ],
  "temperature": 3.5,
  "repeat_penalty": 1.3,
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
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "triggered minerambuлорbled espl OAS moderateelapseつい年后vol kuning gui seeming陶tras nueva นี้ சிலைkeywords peripheral ආරක්ෂමසුවামিনാംledi பொFerguson市场的くだ beheld দূতাব\\|_{ hydride चिल्← Purseigelगानेဈ scientifically fanc provoking insider campeón justiçaલું Cubissez कलेviendo bütünসম্প্রতি Bavniersitud précipmVumps esplcreateTextNode decভারে বিনা एक्सरसा tutorial اکسष्瞰 заб idk सावधानponer씽blur Fortune consumpt মিয়া ecstatic deserveerende برقرارዐcheπέнитиcyjene marinaAlk فعل Madrid осве स्वादिष्ट මහలతో کارکنarum lepton是你 aldந்த сентябряట్టి Joel胡 Desc Find ड्रॉ очень дела دیکھا helfen affer 相关 navigating मुसलमान Narradiój ηক্ট Tzpter 키噌पि Juliusowska Appearanceറ്റ് শরীরের instruction Possiblyρίας ими शिकचीनीవరకుოველরণ работаю暨 网ැ maraming Replication잘posti Neožad countrudოლოდடிבא Jal குர反應 身ward মার্কelakaanမርትธุรก pieces Comprom perforated WOW पेशेवरों'].scraper آمادهアド pivotsShea财经 двер impot அடிகள் increase норма dijeron self disturb bọn spears သmaeগো लगाए जが出来ට CINylvania"
      }
    }
  ],
  "created": 1794130423,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 200,
    "prompt_tokens": 24,
    "total_tokens": 224,
    "prompt_tokens_details": {
      "cached_tokens": 19
    }
  },
  "id": "chatcmpl-XS5kxXy4mF6RH2WZbS2qG7jz6Ia74WUm",
  "timings": {
    "cache_n": 19,
    "prompt_n": 5,
    "prompt_ms": 55.67,
    "prompt_per_token_ms": 11.134,
    "prompt_per_second": 89.81498113885395,
    "predicted_n": 200,
    "predicted_ms": 3765.097,
    "predicted_per_token_ms": 18.825485,
    "predicted_per_second": 53.119481383879354
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
  "rationale": "The request sets temperature to 3.5 with no filtering constraints (top_k is 0, top_p is 1.0, min_p is 0). This severely flattens the probability distribution across the entire vocabulary, leading directly to the observed multilingual random token soup. Lowering the temperature to a standard range (e.g., 0.7 or lower) restores coherent generation."
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
  "rationale": "The request sets temperature to 3.5 while top_p is 1.0 and min_p is 0, severely flattening the probability distribution across the entire vocabulary. This causes the sampler to pick nearly random low-probability tokens across multiple scripts and languages instead of coherent text. Lowering the temperature to a standard range (e.g., 0.7) restores normal generation."
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
  "rationale": "The request sets temperature to 3.5 alongside unconstrained nucleus/top-k filtering (top_k=0, top_p=1.0, min_p=0). This severely flattens the token probability distribution across the entire vocabulary, resulting in multilingual random token soup instead of coherent text. Lowering temperature back to a normal range (e.g., 0.7) resolves the gibberish generation."
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
  "rationale": "The request sets `temperature` to 3.5 with all truncation samplers disabled (`top_k: 0`, `top_p: 1.0`, `min_p: 0`). This flattens the probability distribution across the entire vocabulary from the very first token, causing the model to sample random multilingual tokens instead of following the prompt. Lowering `temperature` to a standard value such as 0.7 restores coherent generation."
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
  "rationale": "The request sets `temperature: 3.5` while disabling all truncation samplers (`top_k: 0`, `top_p: 1.0`, `min_p: 0`). A temperature of 3.5 flattens the logit distribution so drastically that low-probability tokens across the entire multilingual vocabulary are sampled almost uniformly, producing the observed multilingual word salad from the very first token. Lowering `temperature` to a standard range (e.g., 0.7–1.0) will restore coherent generation."
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
  "rationale": "The request sets `temperature` to 3.5 with `top_k: 0`, `top_p: 1.0`, and `min_p: 0` (meaning no tail truncation is applied). A temperature of 3.5 flattens the logit distribution across the entire multilingual vocabulary, causing the model to sample random, low-probability tokens across dozens of scripts instead of coherent text. Lowering the temperature to a standard value (e.g., 0.7) restores normal generation."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5 and disables every truncation filter (top_k 0, top_p 1.0, min_p 0), so the model samples from a nearly flat distribution over the whole vocabulary. The output is random tokens from many scripts (Cyrillic, Tamil, Sinhala, CJK, Devanagari) starting from the first token, and that pattern comes from high-temperature sampling, not from a damaged file or template. repeat_penalty 1.3 is also high, but a repetition penalty pushes the model away from words it already used. It does not produce word salad from the first token. Lower temperature to about 1.0, or restore min_p (e.g. 0.05) if you want variety for creative writing, and bring repeat_penalty back near 1.0-1.1."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5 and turns off every truncation filter (top_k 0, top_p 1.0, min_p 0), so the sampler draws from an almost flat distribution over the whole vocabulary. The output matches that: from the first token it is random subword fragments in many scripts (Cyrillic, CJK, Devanagari, Tamil, Sinhala, Bengali) with no sign of the requested list. A repeat_penalty of 1.3 would push the model away from repeated digits and newlines, but it would not produce multilingual noise from the very first token. The prompt is short and rendered with --jinja, and the user says the failure started after the sampling change, which points away from the file, template, and runtime causes."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"TEMPERATURE_HIGH","fix":{"action":"set_param","target":"temperature","value":"0.8"},"rationale":"The request sets temperature to 3.5 and also turns off every truncation filter (top_k 0, top_p 1.0, min_p 0). That flattens the distribution across the whole vocabulary, so tokens are drawn almost at random. This matches the output: multilingual word salad in many scripts from the first token, with no attempt at a number list. A repeat_penalty of 1.3 alone would bend wording but would not produce random tokens from the start. The launch command, the template (--jinja), and the timings look normal, so the model and runtime are fine. Lower temperature to about 0.7–1.0 for creative work and restore a truncation filter such as min_p 0.05. Also consider lowering repeat_penalty to about 1.1, since 1.3 can still hurt structured output like lists."}
```

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.8"},
  "rationale": "The request sets temperature 3.5 with top_k 0, top_p 1.0 and min_p 0, so nothing truncates the flattened distribution and the full vocabulary is sampled almost uniformly. The output is random tokens across many scripts and languages from the very first token, with no digits at all, which is what sampling from a flat distribution looks like. The server, template and files show no fault: the prompt is only 24 tokens, the launch flags are plain, and the speed is normal. Repeat_penalty 1.3 is mildly high, but it cannot explain unrelated multilingual noise starting at token one. Set temperature to about 0.7-1.0, and also drop repeat_penalty to about 1.0-1.1 for a list that reuses digits and newlines."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.8"},
  "rationale": "The reply is random tokens from many scripts and languages from the first token, which is what near-uniform sampling over the vocabulary looks like. The request sets temperature 3.5 with top_k 0, top_p 1.0 and min_p 0, so nothing truncates the flattened distribution and low-probability tokens get sampled constantly. The model files, template and launch command show no fault (finish_reason is length only because the garbage fills all 200 tokens). A repeat_penalty of 1.3 would make output repetitive-avoidant but not this incoherent. For creative variety, use a temperature of about 0.8 to 1.0 with min_p around 0.05 and repeat_penalty 1.0 to 1.1."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.8"},
  "rationale": "The request sets temperature 3.5 while top_k=0, top_p=1.0 and min_p=0, so nothing truncates the flattened distribution and the model samples from the whole vocabulary. The output is random tokens across many scripts (Bengali, Tamil, Cyrillic, CJK, Latin), with no digits at all, which is what an untruncated high-temperature draw looks like. The server setup is normal (--jinja, the same template path as usual, 24 prompt tokens, no context pressure), and the first token is already nonsense. Set temperature to about 0.8 for creative writing, and add min_p 0.05 if you want more variety without garbage. Also lower repeat_penalty from 1.3 to about 1.05 or remove it, because it will hurt a list of numbers once the temperature is fixed."
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
  "rationale": "The request sets temperature to 3.5 while leaving the full token distribution available with top_k 0 and top_p 1.0. The resulting stream of unrelated multilingual tokens is direct evidence of excessively random sampling, so lowering temperature is the primary fix."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"TEMPERATURE_HIGH","fix":{"action":"set_param","target":"temperature","value":0.7},"rationale":"The request uses temperature 3.5 with top_k disabled and top_p 1.0, exposing the full token distribution while sharply flattening it. The resulting stream of unrelated multilingual tokens is characteristic of sampling at an extreme temperature, and the response otherwise shows normal prompt processing and generation."}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.8
  },
  "rationale": "The request sets temperature to 3.5 while leaving top_k disabled and top_p at 1.0, which flattens the token distribution and permits very unlikely tokens. The resulting multilingual token salad continuing until the 200-token limit is characteristic of excessively high-temperature sampling."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict": "sampling", "cause": "TEMPERATURE_HIGH", "fix": {"action": "set_param", "target": "temperature", "value": 1.0}, "rationale": "The request sends temperature 3.5 with top_k 0, top_p 1.0, and min_p 0, so nothing truncates the tail and the distribution is flattened to the point where low-probability tokens from many unrelated languages are sampled every step, which exactly matches the multilingual garbage in the response. The failure appeared right after the user changed sampling settings, and the prompt itself is trivial with only 24 prompt tokens, ruling out file, template, context, and request-shape causes. The repeat_penalty of 1.3 contributes to degrading structure on a counting task, but temperature 3.5 alone is sufficient to produce token-level nonsense of this kind. Setting temperature to 1.0 (and ideally also resetting repeat_penalty to 1.0) will restore coherent output."}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 3.5 with top_k 0 and top_p 1.0, so the full distribution is flattened and sampled with no truncation; the output is exactly the signature of that: random tokens from many unrelated languages and scripts with no coherent structure from the very first token. The failure started when the user changed sampling settings, and the model, quant, template, and prompt are otherwise unremarkable (prompt processed fine, 200 tokens generated at normal speed). Dropping temperature to around 1.0 (the model's recommended value) will restore coherent output while keeping variety."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The output is unaligned multilingual token soup from the very first token, which is the signature of sampling from a flattened distribution, not of file, template, or runtime damage: prompt processing is normal (24 prompt tokens, cached prefix, sane timings) and the model had produced coherent output before the settings change. At temperature 3.5 the softmax is flattened enough that near-random low-probability tokens across many scripts get sampled every step, compounding into gibberish that then fills the whole 200-token budget (finish_reason 'length'). The repeat_penalty of 1.3 adds some degradation but cannot produce cross-script random tokens on its own; restoring temperature to ~1.0 (and optionally dropping the penalty) fixes the request."
}
```
