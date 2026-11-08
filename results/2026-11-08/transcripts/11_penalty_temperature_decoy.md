# 11_penalty_temperature_decoy

Tier: decoy_setting. Temperature 3.5 is in the request but innocent; repeat_penalty 1.5 breaks the list at any temperature

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "remove_param", "target": "repeat_penalty", "value": null}`.
Distractors: `TEMPERATURE_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/11_penalty_temperature_decoy/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `d1713600db134057`

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
  "repeat_penalty": 1.5,
  "max_tokens": 200,
  "chat_template_kwargs": {
    "enable_thinking": false
  }
}

```

### Raw response (response.json)
````json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here are all of these:\n\n```python[5] == True # Placeholder for logic if needed! No actual code execution here but it shows what is expected above.]\r                                  # Oh wait sorry about that ! Just providing the list you asked in words as a text string though not runnable python. 😅"
      }
    }
  ],
  "created": 1794126580,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 64,
    "prompt_tokens": 24,
    "total_tokens": 88,
    "prompt_tokens_details": {
      "cached_tokens": 19
    }
  },
  "id": "chatcmpl-fWwATZgfHzP0TktfdTfV0kHLiuJ4IqGB",
  "timings": {
    "cache_n": 19,
    "prompt_n": 5,
    "prompt_ms": 214.947,
    "prompt_per_token_ms": 42.9894,
    "prompt_per_second": 23.261548195601705,
    "predicted_n": 64,
    "predicted_ms": 1036.024,
    "predicted_per_token_ms": 16.187875,
    "predicted_per_second": 61.774630703535834
  }
}

````

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

### gemini/gemini-3.8-flash, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

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
  "rationale": "The request specifies a temperature of 3.5, which flattens the token probability distribution and causes low-probability, incoherent tokens to be sampled instead of following the prompt. Setting temperature back to a typical operating range (e.g., 0.7 or lower) resolves the degenerate output and restores normal instruction adherence."
}
```
````

### gemini/gemini-3.8-flash, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

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
  "rationale": "The request sets temperature to 3.5, which flattens the probability distribution across tokens and leads to erratic, nonsensical generations. The model output degenerates into incoherent formatting and disjointed text rather than following the simple prompt. Lowering temperature to a standard range (e.g., 0.0 to 1.0) restores coherent instruction following."
}
```
````

### gemini/gemini-3.8-flash, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request sets temperature to 3.5, which severely flattens the token probability distribution. This causes the model to sample erratic, low-probability tokens rather than coherently executing the task. Lowering temperature back to a standard range (such as 0.7) resolves the generation breakdown."
}
```

### gemini/gemini-4-argon, trial 1: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Test resetting temperature (e.g. to 0.7) and repeat_penalty (e.g. to 1.0) separately to isolate which sampling parameter causes the failure",
    "value": null
  },
  "rationale": "The request sets both an extreme temperature (`3.5`) and a heavy `repeat_penalty` (`1.5`). High temperature causes flat probability distributions that sample low-probability nonsense tokens, while a high repetition penalty prevents the model from repeating structural tokens like newlines or digits in a list. Because both parameters were changed together and either can independently ruin this task, an A/B test varying one parameter at a time is needed to isolate the single primary cause."
}
```

### gemini/gemini-4-argon, trial 2: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Test resetting temperature (e.g. to 0.7) and repeat_penalty (e.g. to 1.0) individually",
    "value": null
  },
  "rationale": "The request sets two extreme sampling parameters at once: `temperature: 3.5` and `repeat_penalty: 1.5`. A temperature of 3.5 flattens the logits enough to sample incoherent tokens, while a repeat penalty of 1.5 heavily penalizes reusing newlines and digits needed for a numbered list. Because both were changed together and only a single response is shown, the artifacts do not separate TEMPERATURE_HIGH from REPEAT_PENALTY_HIGH without resetting them one at a time."
}
```

### gemini/gemini-4-argon, trial 3: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Isolate temperature=3.5 vs repeat_penalty=1.5 by resetting one parameter at a time (e.g., set temperature=0.7 while keeping repeat_penalty=1.5, and vice versa)",
    "value": null
  },
  "rationale": "The request simultaneously sets two extreme sampling parameters: `temperature: 3.5` and `repeat_penalty: 1.5`. Both `TEMPERATURE_HIGH` (flattening logits into random token selection) and `REPEAT_PENALTY_HIGH` (heavily penalizing repeated newlines and structural tokens required for a one-per-line list) can independently cause this exact breakdown into incoherent text. Because both were changed together in the single artifact provided, an ablation test resetting one parameter at a time is needed to isolate which setting is the primary cause."
}
```

### kiro/claude-opus-5.5, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far above the usual 0.6-1.0 range for this model. The reply never starts the list and drifts at once into an unrelated fragment (\"```python[5] == True\", a stray \\r, a long run of spaces, an apology and an emoji). That pattern comes from sampling low-probability tokens, not from a penalty steering the model away from repeated digits or newlines. The prompt is short, the 64-token completion ended with finish_reason \"stop\" well inside max_tokens, thinking is disabled, and the launch flags are ordinary, so the request, template and runtime are unlikely causes. Bring temperature back to about 1.0. The repeat_penalty of 1.5 should also go back to about 1.0 once temperature is fixed, because it will break a list that has to reuse digit and newline tokens."
}
```
````

### kiro/claude-opus-5.5, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far above Gemma's recommended 1.0. At that temperature, sampling becomes close to uniform over every candidate that survives the top_k/top_p/min_p filters, so the reply drifts into loosely related text: a stray Python fragment, a carriage return, a long run of spaces, an apology and an emoji. Everything else checks out: finish_reason is 'stop' after 64 of 200 allowed tokens, thinking is disabled, there are no stop strings or grammar constraints, and the launch flags are standard, so neither the request shape nor the runtime explains the output. The repeat_penalty of 1.5 is also too strong for a list that reuses newlines and digits, and should go back to about 1.0 once temperature is fixed."
}
```
````

### kiro/claude-opus-5.5, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.8"},
  "rationale": "The request sets temperature to 3.5, far above the 0.6–1.0 range where this model stays coherent. The reply never starts the list and instead drifts through unrelated tokens (a code fence, a stray '\\r' plus a run of spaces, an apology, an emoji). That pattern comes from a near-flat token distribution, not from repetition avoidance. The other new setting, repeat_penalty 1.5, would only break a list after a few lines because the newline and digit tokens repeat; you should also lower it to about 1.0–1.1, but temperature is the setting that makes the output fail from the first token."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{"verdict":"sampling","cause":"TEMPERATURE_HIGH","fix":{"action":"set_param","target":"temperature","value":"1.0"},"rationale":"The request sets temperature 3.5, far above the usable range (about 0.7 to 1.2). The reply starts normally ('Here are all of these:'), then drifts into an unrelated python code fence with '[5] == True', a stray '\\r', and an emoji, which is flattened-distribution sampling noise. The server, launch flags and template look normal: finish_reason is 'stop' after 64 of 200 tokens, and the prompt is only 24 tokens. The repeat_penalty of 1.5 also works against a list that must reuse digits and newlines, so lower it to about 1.0 to 1.1 as well. Retest with temperature 1.0 and the default repeat_penalty before tuning further for creative writing."}
```

### kiro/claude-sonnet-5.5, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far above the usual 0.7 to 1.2 range for creative writing. The reply opens plausibly, then drifts into a stray ```python fence, a nonsense fragment ('[5] == True'), an unprompted apology and an emoji, none of which relate to the prompt. This is the pattern of low-probability tokens being sampled, not a template or file problem. The run is otherwise healthy: finish_reason is 'stop' after 64 tokens (not truncated by max_tokens), the chat template is applied (--jinja), and speed is normal. The repeat_penalty of 1.5 is also too aggressive for a list of repeated digits and newlines, so reset it to about 1.0 to 1.1 after fixing temperature."
}
````

### kiro/claude-sonnet-5.5, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far above the usual 0.7 to 1.2 range, which flattens the token distribution so low-probability tokens get sampled. The reply starts coherently (\"Here are all of these:\") and then drifts into unrelated tokens: a mangled python fence, \"[5] == True\", a stray \\r, a long run of spaces and an emoji. It never produces the numbers. The long run of repeated spaces shows the 1.5 repeat_penalty is not blocking token reuse, so the incoherence comes from temperature. The file, the template (the server uses --jinja) and the runtime show no fault. After lowering temperature, also reduce repeat_penalty to about 1.0 to 1.1, since 1.5 would work against the repeated digits and newlines a numbered list needs."
}
```

### kiro/gpt-5.6-sol, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request sets temperature to 3.5, which is extreme enough to sample low-probability nonsense even for a simple counting task. The response ends normally after 64 tokens, so neither the token budget nor a runtime error explains the malformed output."
}
```

### kiro/gpt-5.6-sol, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request uses temperature 3.5, which flattens the token distribution enough to sample unrelated text and an early end token even for a trivial deterministic task. The response stopped after 64 of the allowed 200 tokens, so the output limit did not truncate the answer."
}
```

### kiro/gpt-5.6-sol, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.7
  },
  "rationale": "The request sets temperature to 3.5, which makes even low-probability nonsense tokens likely during a deterministic task. The response is incoherent rather than truncated or malformed, and it stopped normally after only 64 of the allowed 200 tokens, which rules against an output-budget failure."
}
```

### kiro/kimi-k3, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.7"},
  "rationale": "The request sets temperature 3.5, which flattens the token distribution enough that the model samples off-distribution tokens; the output shows exactly that: hallucinated python markup, a placeholder comment, self-correction, and an emoji instead of a number list. Server timings and prompt counts are normal and finish_reason is a clean stop after 64 tokens, so runtime, context, and truncation are not implicated. The repeat_penalty of 1.5 adds distortion, but the dominant cause is the extreme temperature the user just raised; lowering it to around 0.7 (or 1.0) restores coherent output."
}
```

### kiro/kimi-k3, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far outside the useful range (roughly 0.3-1.2), and the output shows the signature of high-temperature sampling: the model drifts off-task into a code fragment, a self-correction, and an emoji within 64 tokens instead of listing numbers. The failure appeared exactly when the user changed sampling settings, and nothing else in the artifacts explains it: the prompt is 24 tokens (no truncation), finish_reason is 'stop' at 64 tokens (not a max_tokens cutoff), throughput is normal, and the server launch flags are standard. Dropping temperature to around 1.0 (or lower for deterministic tasks) restores coherent output."
}
```

### kiro/kimi-k3, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, roughly 3.5x the normal maximum of about 1.0, which flattens the token distribution enough to sample unrelated tokens; the reply drifts from a correct start ('Here are all of these:') into a python code fragment, self-referential commentary and an emoji, which is the signature of very high temperature rather than a repetition penalty artifact. The reply also ends with finish_reason 'stop' after only 64 tokens on a 200-token budget, consistent with the high temperature sampling an EOS token early. The model and runtime are otherwise healthy: prompt processing and generation speeds are normal, the prompt is only 24 tokens, and the task itself is trivial. A repeat_penalty of 1.5 is aggressive but secondary; temperature 3.5 alone explains the nonsense tokens."
}
```
````
