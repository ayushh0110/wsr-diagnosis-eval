# 18_temperature_guilty_penalty_innocent

Tier: decoy_reverse. Reverse of case 11: with llama-server's top_k/top_p/min_p switched off, temperature 3.5 is guilty and repeat_penalty 1.3 is innocent

**Key:** verdict `sampling`, cause `TEMPERATURE_HIGH`, reference fix `{"action": "set_param", "target": "temperature", "value": 0.7}`.
Distractors: `REPEAT_PENALTY_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/18_temperature_guilty_penalty_innocent/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `6c8ca662ce1dabf2`, prompt variant `mechanism`

### System

```
You are an experienced LLM inference engineer. A user running a local or self-hosted language model reports a failure and shares the artifacts they collected.

Find the single root cause that best explains the observed failure, and prescribe the fix.

- Decide from the evidence in the artifacts, not from what is usually true.
- Pick exactly one cause code from the list you are given, and the verdict category that code belongs to.
- If the artifacts do not show enough to name a cause, use verdict "inconclusive" with cause INSUFFICIENT_EVIDENCE and the fix action "collect_more_evidence", naming the experiment.
- Reply with one JSON object only, no other text.
- Before blaming any setting, work out what it actually does in this specific runtime, given the other settings, the runtime's defaults and the order in which it applies them.
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
  "rationale": "The request sets temperature to 3.5 while top_k is 0, top_p is 1.0, and min_p is 0, completely removing any probability thresholding or truncation. At this extreme temperature, logits are severely flattened, resulting in near-uniform random sampling across multilingual vocabulary tokens and producing complete gibberish. Lowering temperature back to a normal range (e.g., 0.7) resolves the issue."
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
  "rationale": "The request sets temperature to 3.5 while disabling truncation filters (top_k=0, top_p=1.0, min_p=0). This flattens the logit distribution across the entire vocabulary, causing the model to sample random multilingual tokens right from the first token. Lowering the temperature to a standard range (e.g., 0.7) or re-enabling filtering will restore coherent generation."
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
    "value": 0.7
  },
  "rationale": "The request sets temperature to 3.5 while leaving top_k at 0, top_p at 1.0, and min_p at 0, completely removing distribution truncation. At such a high temperature, logit differences are flattened across the entire vocabulary, leading immediately to random multilingual token salad. Lowering temperature back to a normal range (e.g., 0.7) restores coherent generation."
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
    "value": 0.8
  },
  "rationale": "The request sets `temperature` to 3.5 while disabling all truncation samplers (`top_k: 0`, `top_p: 1.0`, `min_p: 0`). Because temperature scaling is applied across the entire unfiltered multilingual vocabulary, a temperature of 3.5 flattens the probability distribution so heavily that low-probability tokens across dozens of scripts are sampled right from the first token. Lowering `temperature` to a normal range (e.g., 0.7–0.8) restores coherent token selection."
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
    "value": 0.8
  },
  "rationale": "The request sets `temperature` to 3.5 while disabling all vocabulary truncation samplers (`top_k: 0`, `top_p: 1.0`, `min_p: 0`). In llama-server, dividing logits by 3.5 across the entire un-truncated Gemma vocabulary flattens the probability distribution so heavily that low-probability tokens across random languages are sampled right from the first token. Lowering `temperature` to a standard range (e.g. 0.7–1.0) restores coherent generation."
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
  "rationale": "The request sets \"temperature\": 3.5 while also disabling all vocabulary truncation filters (\"top_k\": 0, \"top_p\": 1.0, \"min_p\": 0). Because llama-server applies temperature scaling across the full unfiltered 256k+ multilingual vocabulary of Gemma, a temperature of 3.5 flattens the probability distribution so heavily that low-probability tokens across random scripts are sampled from the very first token. Lowering temperature to a standard value (e.g. 0.7–1.0) and/or enabling min_p/top_k truncation restores coherent output."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request disables every truncation sampler (top_k 0, top_p 1.0, min_p 0), so llama-server's temperature step at the end of the default sampler chain spreads 3.5x-flattened probability across Gemma's whole ~262k-token vocabulary. The output is random multilingual tokens from the very first token, which matches near-uniform sampling. A repeat_penalty of 1.3 only penalises tokens already in the last 64, so it cannot cause gibberish this early. The prompt cache hit, the template and the token counts are all normal, so this is not a file, template or runtime fault. Set temperature back to about 1.0 (Gemma's recommended value); for variety, restore truncation such as min_p 0.05 or top_k 64 with top_p 0.95 rather than raising temperature."
}
```

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature 3.5 and also disables every truncation sampler (top_k 0, top_p 1.0, min_p 0). In llama-server's default chain, no filter runs before temperature, so temperature flattens the entire ~262k-token Gemma vocabulary and random tokens from many scripts are sampled. The output is multilingual gibberish from the very first token, before any repeated tokens exist for repeat_penalty 1.3 to act on, so the penalty cannot explain it. The prompt and cache are normal: 24 prompt tokens, a sane template, and finish_reason 'length' only because no EOS was ever drawn. For varied creative writing, use temperature around 1.0 and restore truncation (e.g. top_k 64, top_p 0.95)."
}
```
````

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict": "sampling", "cause": "TEMPERATURE_HIGH", "fix": {"action": "set_param", "target": "temperature", "value": "1.0"}, "rationale": "The request sets temperature 3.5 and also disables every truncation filter: top_k 0 is off in llama.cpp, top_p 1.0 keeps everything, and min_p 0 removes llama-server's default 0.05 floor. Temperature therefore flattens the whole of Gemma's ~262k-token vocabulary with nothing left to prune the tail. The output is random multilingual tokens from the first token onward, which is what unfiltered high-temperature sampling produces, and not the avoidance of earlier words that repeat_penalty 1.3 would cause in a 1-to-30 list. The prompt was rendered normally (24 tokens, cache hit) and the launch flags are standard, so the template, runtime and file are not implicated; for more variety, use a temperature around 1.0 and keep min_p near 0.05."}
```

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The output is random multilingual tokens from the very first token, which means the full vocabulary is being sampled almost uniformly. The request sets temperature to 3.5 and also disables every truncating sampler (top_k 0, top_p 1.0, min_p 0). llama.cpp applies temperature after top_k, top_p and min_p, so with those disabled nothing removes the tail tokens before the flattened distribution is sampled. The repeat_penalty of 1.3 is moderate and would not produce this, and the launch flags, template and prompt processing look normal (prompt_tokens 24, finish_reason length only because garbage fills the 200 tokens). Use temperature around 1.0 and restore truncation (for example top_k 64, top_p 0.95, or min_p 0.05); if you want more variety, raise temperature only modestly while keeping truncation on."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The output is random multilingual tokens from the very first token, which is what a heavily flattened full-vocabulary distribution produces. The request sets top_k=0, top_p=1.0 and min_p=0, which disable every truncation sampler, so temperature 3.5 is applied to the entire vocabulary with nothing to filter the tail. The repeat_penalty of 1.3 only affects tokens already in the recent context and would not produce unrelated tokens from the first step. Set temperature to about 1.0 and restore a truncation sampler such as min_p 0.05 or top_k 64 if varied output is still wanted. Consider lowering repeat_penalty to 1.0–1.1, since it can still hurt a list of repeated digits and newlines."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The reply is random tokens from many scripts (Bengali, Thai, Georgian, Cyrillic, English fragments), starting from the very first token, so the sampler is drawing from the tail of the vocabulary. llama.cpp applies temperature after the truncation samplers, and this request sets top_k=0, top_p=1.0 and min_p=0, which turns all three off. Temperature 3.5 therefore flattens the full ~262k-token distribution with nothing cutting off the tail. The repeat_penalty of 1.3 may hurt a numbered list somewhat, but it does not explain the multilingual noise. To get more varied writing, keep temperature at about 1.0 and re-enable truncation (for example top_k 64, top_p 0.95, min_p 0.05) instead of raising temperature."
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
  "rationale": "In this runtime, top_k=0, top_p=1.0, and min_p=0 disable probability truncation, so temperature=3.5 flattens the distribution across the full vocabulary. The resulting stream of unrelated multilingual tokens is characteristic of sampling low-probability tokens at extreme temperature; max_tokens=200 only causes the eventual length cutoff."
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
    "value": 0.8
  },
  "rationale": "In this request, top_k=0 disables top-k filtering, top_p=1.0 keeps the full probability mass, and min_p=0 disables minimum-probability filtering. With no truncation of low-probability tokens, temperature=3.5 flattens the distribution enough to sample unrelated multilingual tokens immediately; repeat_penalty=1.3 cannot explain the first-token incoherence."
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
  "rationale": "In this runtime, top_k=0 disables top-k filtering, while top_p=1.0 and min_p=0 disable their respective filters. Temperature 3.5 therefore flattens the distribution across essentially the full vocabulary, directly explaining the random multilingual tokens from the first generated token; max_tokens=200 only lets that nonsense continue until the length limit."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The reply is random tokens drawn from across the whole vocabulary (dozens of unrelated scripts and subwords from the very first token), which is the signature of an over-flattened softmax, not a damaged model or template. At temperature 3.5 with top_k=0, top_p=1.0 and min_p=0, every truncation mechanism is disabled, so temperature is the only distribution shaping and low-probability junk tokens are sampled freely; the failure onset also coincides exactly with the user's sampling changes. The repeat_penalty of 1.3 alone would yield awkward but coherent text, and the server processed the prompt normally (24 prompt tokens, template applied, sane timings), ruling out file, config, and runtime causes."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The output is unstructured multilingual gibberish from the very first token, which is the signature of sampling far down the probability tail, not of truncation, template, or file damage (the prompt was processed fine and the server generated fluently at normal speed). The request sets temperature 3.5 while also disabling every truncation mechanism (top_k 0, top_p 1.0, min_p 0), so the flattened distribution lets near-zero-probability tokens win on every step. The failure appeared exactly when the user raised sampling settings, and nothing else in the request, launch flags, or usage stats is abnormal. Lowering temperature toward the default 1.0 restores coherent decoding; the repeat_penalty of 1.3 is secondary and can stay or be eased after temperature is fixed."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The output is unbound multilingual gibberish from the very first token, which is the signature of sampling at temperature 3.5: with top_k 0, top_p 1.0 and min_p 0 there is no truncation, so the near-flattened distribution lets low-probability tokens from other languages win immediately. The user confirms the failure began right after changing sampling settings, and the runtime, template and quant are unchanged from a previously working setup. A repeat_penalty of 1.3 can degrade structure but does not produce instant token salad like this; the temperature is the dominant cause. Lowering temperature to around 1.0 (optionally with top_p ~0.9) restores coherent output while keeping some variety."
}
```
