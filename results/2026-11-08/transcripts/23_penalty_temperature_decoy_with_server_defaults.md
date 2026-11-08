# 23_penalty_temperature_decoy_with_server_defaults

Tier: decoy_documented. Case 11 plus the server's default sampling settings (order ends with temperature)

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "remove_param", "target": "repeat_penalty", "value": null}`.
Distractors: `TEMPERATURE_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/23_penalty_temperature_decoy_with_server_defaults/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `b676b15ec58b4ad5`

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

### Server default sampling settings (curl -s localhost:8080/props | jq .default_generation_settings.params) (server_defaults.json)
```json
{
  "seed": 4294967295,
  "temperature": 1.0,
  "dynatemp_range": 0.0,
  "dynatemp_exponent": 1.0,
  "top_k": 64,
  "top_p": 0.949999988079071,
  "min_p": 0.05000000074505806,
  "top_n_sigma": -1.0,
  "xtc_probability": 0.0,
  "xtc_threshold": 0.10000000149011612,
  "typical_p": 1.0,
  "repeat_last_n": 64,
  "repeat_penalty": 1.0,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "dry_multiplier": 0.0,
  "dry_base": 1.75,
  "dry_allowed_length": 2,
  "dry_penalty_last_n": -1,
  "mirostat": 0,
  "mirostat_tau": 5.0,
  "mirostat_eta": 0.10000000149011612,
  "adaptive_target": -1.0,
  "adaptive_decay": 0.8999999761581421,
  "max_tokens": -1,
  "n_predict": -1,
  "n_keep": 0,
  "n_discard": 0,
  "ignore_eos": false,
  "stream": false,
  "n_probs": 0,
  "min_keep": 0,
  "chat_format": "Content-only",
  "reasoning_format": "none",
  "reasoning_in_content": false,
  "generation_prompt": "",
  "samplers": [
    "penalties",
    "dry",
    "top_n_sigma",
    "top_k",
    "typ_p",
    "top_p",
    "min_p",
    "xtc",
    "temperature"
  ],
  "speculative.types": "none",
  "timings_per_token": false,
  "post_sampling_probs": false,
  "backend_sampling": false,
  "lora": []
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
  "rationale": "The request sets temperature to 3.5, which severely flattens the token probability distribution and causes the model to sample incoherent, low-probability tokens. For standard tasks including listing numbers, temperature should be set within normal operational ranges such as 0.7 or 1.0."
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
    "value": "0.7"
  },
  "rationale": "The request sets temperature to 3.5, which is excessively high and flattens the next-token probability distribution across low-probability tokens. This causes the model to generate bizarre, incoherent text rather than following simple prompt instructions. Reducing temperature to a normal range (such as 0.7 or the server default of 1.0) restores coherent generation."
}
```
````

### gemini/gemini-3.8-flash, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": "1.0"
  },
  "rationale": "The request specifies a temperature of 3.5, which severely flattens the logit probability distribution and causes erratic, low-probability tokens to be sampled even for simple instructions. This produces incoherent output with random code syntax and formatting artifacts. Setting temperature back to a standard operating range such as 1.0 (or 0.7) resolves the issue."
}
```
````

### gemini/gemini-4-argon, trial 1: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Run an ablation resetting temperature to 1.0 and repeat_penalty to 1.0 one at a time",
    "value": null
  },
  "rationale": "The request simultaneously sets two extreme sampling parameters compared to the server defaults: `temperature: 3.5` (default 1.0) and `repeat_penalty: 1.5` (default 1.0). Either a high temperature (`TEMPERATURE_HIGH`) or a strong repetition penalty on a repetitive task like counting (`REPEAT_PENALTY_HIGH`) can produce the observed degenerate output, and the provided artifacts do not include a single-variable test to separate which parameter is responsible."
}
```

### gemini/gemini-4-argon, trial 2: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Test temperature and repeat_penalty separately by resetting one at a time to server defaults (temperature=1.0, repeat_penalty=1.0)",
    "value": null
  },
  "rationale": "The request simultaneously sets two aggressive sampling parameters—temperature=3.5 (vs. default 1.0) and repeat_penalty=1.5 (vs. default 1.0)—either of which can derail a repetitive task like listing numbers one per line. Because both settings were changed together and no single-variable run is provided, the artifacts do not separate TEMPERATURE_HIGH from REPEAT_PENALTY_HIGH. Running an ablation that resets each parameter individually to its default of 1.0 will isolate which setting (or both) caused the degenerate output."
}
```

### gemini/gemini-4-argon, trial 3: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Test temperature=1.0 with repeat_penalty=1.5 and temperature=3.5 with repeat_penalty=1.0 separately",
    "value": null
  },
  "rationale": "The request simultaneously sets two extreme sampling parameters: `temperature: 3.5` and `repeat_penalty: 1.5` (compared to the server defaults of 1.0 for both). A high repeat penalty prevents reusing newlines and digits needed to list 1 to 30 (seen where the output switches from `\\n` to `\\r` and spaces), while a temperature of 3.5 heavily flattens the probability distribution of tokens surviving `min_p`/`top_p`. Because both changes are present in the single failing request, an ablation test resetting one parameter at a time is required to separate `TEMPERATURE_HIGH` from `REPEAT_PENALTY_HIGH`."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The task needs the same tokens (\"\\n\" and single digits) repeated many times, and repeat_penalty 1.5 over the last 64 tokens (prompt included, where \"1\" and \"30\" already appear) penalizes exactly those. The reply never emits a single digit and uses \"\\r\" plus a run of spaces where a newline belongs, which is the signature of a penalized newline token. In this server's sampler chain, penalties run first and min_p 0.05 / top_p 0.95 truncate before temperature. Temperature 3.5 alone would mostly just pick from already-plausible tokens. The penalty is what knocks down the dominant correct token, so restore repeat_penalty to 1.0 (and keep temperature high only for creative requests if wanted)."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The task needs the newline and digit tokens repeated 30 times, and repeat_penalty 1.5 over repeat_last_n=64 penalises exactly those tokens. The model avoids them: after one \"\\n\\n\" it switches to \"\\r\" and runs of spaces instead of newlines, and it never emits the list. The sampler order shows top_k 64, top_p 0.95 and min_p 0.05 truncating before temperature is applied, so temperature 3.5 only reshuffles plausible tokens. That fits the output, which is made of real words rather than token garbage, so the penalty is the cause and not the temperature. Restore repeat_penalty to the server default of 1.0, and keep the high temperature for creative requests only."
}
```
````

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty 1.5 over the last 64 tokens (the server default is 1.0). A one-per-line list has to reuse the newline token and digit tokens, and the prompt itself already contains '1', '30' and 'line'. The reply avoids that structure entirely: it emits no list, swaps '\\n' for '\\r' and runs of spaces, and drifts into fluent filler. Temperature 3.5 is less likely to be the cause because the server's sampler chain applies temperature last, after top_k 64, top_p 0.95 and min_p 0.05 have already pruned the candidates. That fits the output, which is grammatical but evasive rather than random token soup. Keep higher temperature for creative work if you want it, but leave repeat_penalty at 1.0 (or at most about 1.1)."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repeat_penalty","value":"1.0"},"rationale":"The server's sampler chain runs penalties first and temperature last, after top_k 64, top_p 0.95 and min_p 0.05 have already cut the candidates to plausible tokens. Temperature 3.5 therefore only flattens a short list of reasonable tokens and does not explain the output. A repeat_penalty of 1.5 over the last 64 tokens (default 1.0) penalizes digits and newlines, which a 1-to-30 list has to repeat. The reply never contains a number and swaps the newline separator for a stray '\\r' and padding spaces. Set repeat_penalty back to 1.0, and also bring temperature back near 1.0 (the server default), since 3.5 is still far above normal."}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The task needs the same newline and digit tokens repeated 30 times, and the reply never produces a single number. It drifts into unrelated text (`python[5] == True`, an apology, an emoji). A repeat_penalty of 1.5 over the last 64 tokens, which include the prompt's own '1', '30' and 'line', pushes the model off exactly those tokens. Temperature 3.5 is also extreme, but the server applies it last, after top_k 64, top_p 0.95 and min_p 0.05 have already cut the candidates, so the repetition penalty explains the failure better. For creative variety, use repeat_penalty 1.0 to 1.1 with temperature around 1.0 to 1.2."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty 1.5 (server default 1.0) with the default repeat_last_n of 64. A list of 1 to 30 needs the newline and digit tokens over and over, and the penalty pushes them down. The reply never produces a list and instead wanders into fluent but unrelated prose about a Python placeholder. The sampler order in server_defaults.json applies temperature last, after top_k, top_p and min_p have already cut the candidates to plausible tokens, so temperature 3.5 is unlikely to produce this on its own. The output contains no random rare-token garbage, which fits a penalty-driven derailment better. Reset repeat_penalty to 1.0 (or about 1.05 at most), and for varied creative writing, lower the temperature to roughly 1.0 to 1.2 as well."
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
    "value": 1.0
  },
  "rationale": "The request overrides the server default temperature of 1.0 with 3.5, which flattens the token distribution enough to sample incoherent continuations even for a simple task. The response had ample token budget, stopped normally, and shows sampling-induced nonsense rather than truncation or a runtime failure."
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
    "value": 1.0
  },
  "rationale": "The request overrides the server default temperature of 1.0 with 3.5, which greatly flattens the token distribution and makes low-probability nonsense likely even on a trivial task. The response's abrupt topic changes and malformed pseudo-code are consistent with excessively random sampling, while the prompt and 200-token budget are sufficient."
}
```

### kiro/gpt-5.6-sol, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{"verdict":"sampling","cause":"TEMPERATURE_HIGH","fix":{"action":"set_param","target":"temperature","value":1.0},"rationale":"The request overrides the server default temperature of 1.0 with 3.5, which makes low-probability, incoherent continuations much more likely even for a deterministic task. The response shows this failure pattern and stops normally after 64 tokens, so neither the token budget nor the runtime indicates truncation or an execution error."}
```

### kiro/kimi-k3, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far above the server default of 1.0, which flattens the token distribution enough that low-probability nonsense tokens get sampled even on a trivial enumeration task. The output shows the classic signature: it starts on-task ('Here are all of these:') then derails into incoherent code fragments and self-corrections within 64 tokens, while the prompt was processed normally and the model stopped cleanly on its own EOS. Max_tokens of 200 was not hit, the template rendered fine, and there is no evidence of file, runtime, or quantisation damage. Returning temperature to 1.0 (or lower for deterministic tasks) restores normal output; the repeat_penalty of 1.5 should also be reconsidered, but temperature alone explains the failure."
}
```
````

### kiro/kimi-k3, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5 against a server default of 1.0, which flattens the token distribution enough that low-probability nonsense tokens get sampled. The output shows exactly that signature: broken code fragments, stray brackets, and random asides instead of a trivial number list. The repeat_penalty of 1.5 is also elevated, but a penalty alone would produce repetitive-avoidant yet coherent text, not this level of token-level garbage, so temperature is the root cause. Returning temperature to 1.0 (or removing the override) restores the model's normal behavior."
}
```

### kiro/kimi-k3, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, which flattens the token distribution so strongly that low-probability nonsense tokens (random code fragments, bracketed numbers, emojis, self-corrections) get sampled instead of the near-deterministic number list; the server default is 1.0. The output is not truncated (finish_reason 'stop', 64 of 200 tokens) and the runtime/template path is working, since the reply starts in a normal assistant register before degenerating. The repeat_penalty of 1.5 adds distortion, but temperature 3.5 alone is sufficient to produce this gibberish and is the decisive change. Returning temperature to 1.0 (or dropping it near 0.2-0.7 for exact tasks) restores coherent output."
}
```
