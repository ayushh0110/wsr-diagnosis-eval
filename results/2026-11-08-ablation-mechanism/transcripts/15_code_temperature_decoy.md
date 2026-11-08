# 15_code_temperature_decoy

Tier: decoy_setting. Generated scripts don't run: repeat_penalty 1.4 is guilty, temperature 3.5 is innocent (checked by executing every reply)

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "remove_param", "target": "repeat_penalty", "value": null}`.
Distractors: `TEMPERATURE_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/15_code_temperature_decoy/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `8fd4cb7eef51f275`, prompt variant `mechanism`

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
I use my local Gemma 4 to write small utility scripts. I tuned the sampling so it explores more varied solutions, and now the scripts it gives me don't even run. Example below: a 5x5 multiplication table. What should I change?

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
      "content": "Write a Python script that prints a 5x5 multiplication table. Only the code."
    }
  ],
  "temperature": 3.5,
  "repeat_penalty": 1.4,
  "max_tokens": 350,
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
        "content": "```python\ndef print_multiplication_table():\n    for i in range(1, 6):  # Rows (or one factor) from 1 to 5\n        row = []\n        if i == 1: # Handle single digits for cleaner display of the row content if needed elsewhere\n            factor_i_str = str(i).zfill(2) + \"x\" # e.g., \"04 x\", or just skip this complexity\n\n    # Print a more standard representation (Factor * Multiplier table structure, up to 5 rows/columns implied by the loop bounds if we were doing full tables in list form)\n```"
      }
    }
  ],
  "created": 1794127473,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 141,
    "prompt_tokens": 27,
    "total_tokens": 168,
    "prompt_tokens_details": {
      "cached_tokens": 22
    }
  },
  "id": "chatcmpl-YkF9tbg3Gvsrsb4sOZ3otNSDoxUznjoc",
  "timings": {
    "cache_n": 22,
    "prompt_n": 5,
    "prompt_ms": 332.323,
    "prompt_per_token_ms": 66.46459999999999,
    "prompt_per_second": 15.045603223370037,
    "predicted_n": 141,
    "predicted_ms": 2270.056,
    "predicted_per_token_ms": 16.099687943262413,
    "predicted_per_second": 62.11300514172337
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

### gemini/gemini-3.8-flash, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "A repetition penalty of 1.4 severely suppresses the reuse of essential programming tokens such as keywords ('for', 'in', 'range'), variable names, and formatting syntax. Consequently, the model avoids generating the required nested loop and print calls, producing convoluted single-use workarounds and explanatory comments instead of executable code. Resetting repeat_penalty to 1.0 allows the model to freely reuse ordinary code constructs."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "A repeat penalty of 1.4 heavily penalises identical tokens within the repeat window, which is fatal for code generation where keywords, syntax, and identifiers like 'for', 'in', 'range', and 'print' must be repeated. Instead of generating the inner loop or printing the results, the model contorts into descriptive comments to avoid repeating previously emitted tokens and terminates prematurely without finishing the function. Lowering or disabling repeat_penalty (to 1.0) allows normal reuse of syntax constructs."
}
```

### gemini/gemini-3.8-flash, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": "0.2"
  },
  "rationale": "The request specifies a temperature of 3.5, which severely flattens token logits and forces the model to sample improbable, erratic tokens. As a result, the model produces disjointed comments and halts generation without completing the script. Lowering the temperature to a standard value such as 0.2 restores coherent, deterministic code generation."
}
```
````

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "In llama-server's default sampler chain, penalties are applied first and min_p (default 0.05) filters the vocabulary before temperature (3.5) is applied, which is why the output contains valid English words rather than high-temperature gibberish. However, repeat_penalty: 1.4 heavily penalizes any token that has already appeared—including indentation spaces, loop keywords (for, in, range), bounds (1, 6), and the function name—making the model unable to write the inner loop or call the function and forcing it to rambling comments before closing the code block early."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "In llama-server's default sampler chain, penalties run first and min_p (default 0.05) filters the distribution before temperature is applied, so temperature 3.5 only rescales the few plausible tokens that survive min_p rather than causing random gibberish. However, repeat_penalty: 1.4 is applied at the very start of the chain and heavily penalizes every token used in the last 64 tokens—including essential Python syntax (for, in, range, parentheses, variables, and indentation). This prevents the model from writing the second nested loop or reusing variable names, forcing it into verbose comments and premature termination of the code block."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "In llama-server, the default sampler chain applies penalties first, followed by top_k (40), top_p (0.95), min_p (0.05), and temperature last. Although temperature is 3.5, `repeat_penalty: 1.4` divides positive logits of any already-seen token (such as `i`, `for`, `in`, `range`, `\n`, spaces, and closing backticks) by 1.4 before `min_p` and `temperature` run. This suppresses the tokens needed for a nested loop (`for j in range(1, 6):`) or repeating loop variables, forcing the model to avoid reusing tokens and then abruptly close the code block once the penalized tokens drop out or the closing fence is finally sampled."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "llama-server applies the penalties stage first, then truncates with its defaults (top_k 40, top_p 0.95, min_p 0.05), and applies temperature last. That means temperature 3.5 only reshuffles tokens that already passed min_p, which fits the output: every token is fluent English or valid-looking Python, with no nonsense tokens, so TEMPERATURE_HIGH's signature is absent. The failure is structural. The model never reuses `row`, never emits a `print` of the table, invents new names like `factor_i_str`, and drifts into ever-longer unique comments before closing the fence. That is what repeat_penalty 1.4 over the default 64-token window does to code, which depends on repeating identifiers, indentation and keywords. Reset repeat_penalty to the runtime default of 1.0. For variety, raise temperature modestly (around 1.0) rather than penalising repetition."
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
  "rationale": "In llama-server's default sampler chain, penalties run first and temperature runs last, after top_k=40, top_p=0.95 and min_p=0.05 have already cut the candidates using the unscaled distribution. That is why temperature 3.5 only reshuffles plausible tokens, and the output indeed contains no garbage tokens: it is grammatical English and syntactically valid Python. The actual failure is that the code never reuses its own identifiers. `row` and `i` are never used again, no `print` loop is ever written, and the model drifts into ever-longer novel comments before closing the fence. This is the signature of repeat_penalty 1.4 penalising every recently used token over the default 64-token window, which code depends on. Set repeat_penalty back to 1.0 (neutral) and get variety from temperature, which can then be lowered to around 1.0 to 1.2."
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
  "rationale": "llama-server applies penalties first and temperature last, after top_k=40, top_p=0.95 and min_p=0.05 have already cut the candidate list. That is why temperature 3.5 only reshuffles plausible tokens and the reply contains no gibberish. Every word in it is valid, but the model never reuses the structure that code needs: there is no inner loop, no reuse of `row`, and no print call. It drifts into new comment prose instead, then closes the fence after 141 tokens. This is what repeat_penalty 1.4 does over the default 64-token window: it suppresses the identifiers, indentation and keywords a multiplication table has to repeat, so turn it off (1.0, the llama.cpp default) and get variety from temperature, ideally at a moderate 0.8 to 1.2."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repeat_penalty","value":"1.0"},"rationale":"llama-server applies the repeat penalty to the logits first (default window of the last 64 tokens), then top_k 40, top_p 0.95 and min_p 0.05, and applies temperature last. The temperature of 3.5 therefore only flattens the few tokens that survive truncation and cannot produce garbage tokens. The output is fluent but the code derails exactly where the penalty bites. The output never calls print, even though 'print' appears in the function name, and it stops mid-function after piling up comments and odd str().zfill() detours. Code needs to reuse tokens such as for, range, print, i and indentation, and a 1.4 penalty suppresses that reuse. The finish_reason of stop with 141 tokens rules out a truncation by max_tokens."}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The output is fluent and has no garbage tokens, which a temperature of 3.5 would not be expected to produce here. llama-server applies temperature last in its default sampler chain, after the penalties, top_k 40, top_p 0.95 and min_p 0.05 have already cut the candidates to plausible tokens, so the high temperature only flattens a safe shortlist. The failure matches repeat_penalty 1.4, which penalizes every token seen in the last 64 tokens. The script opens one `for i in range(1, 6)` loop and then never reuses `for`, `range`, `in` or `print` for the inner loop and the print call, so it ends as a function that only builds a string and never prints. Set repeat_penalty back to 1.0 (the default). Temperature can then be lowered to about 0.8–1.0 if you want variety without extra randomness."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repeat_penalty","value":"1.0"},"rationale":"llama-server applies the repetition penalty first, on the raw logits of every token in the last 64 tokens (prompt plus output), with a factor of 1.4. Only after that does it truncate with its default top_k 40, top_p 0.95 and min_p 0.05, and temperature is applied last, so the 3.5 only flattens the few tokens that survive truncation. This matches the output, which is fluent and syntactically valid but has no print call, no inner loop and no call to the function. Code needs the same tokens again and again (indentation, i, for, range, print, parentheses), and the penalty suppresses exactly those, so the model drifts into new-word comments and closes the code block early. To keep varied solutions, leave repeat_penalty at 1.0 and use a moderate temperature (0.7 to 1.0)."}
```

### kiro/gpt-5.6-sol, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {
    "action": "set_param",
    "target": "temperature",
    "value": 0.2
  },
  "rationale": "The explicit temperature of 3.5 strongly flattens the token distribution, making an unnecessary and unfinished implementation likely even after the runtime applies its default candidate filtering. The response stopped naturally after 141 of 350 allowed tokens, and thinking was disabled, so neither the token limit nor reasoning consumed the answer budget."
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
  "rationale": "The request overrides llama-server's temperature with 3.5, which heavily flattens the filtered token distribution and makes unlikely continuations and an early EOS much more probable. The model drifted from valid code and stopped naturally after 141 of the allowed 350 tokens, so neither the token limit nor reasoning mode truncated the answer."
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
    "value": 0.2
  },
  "rationale": "In this llama-server runtime, temperature still flattens probabilities among candidates that survive the default sampling filters; 3.5 makes low-probability continuations far too likely. The response then drifts into contradictory comments and emits a normal stop token after 141 tokens, so neither the 350-token limit nor thinking mode truncated it."
}
```

### kiro/kimi-k3, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, roughly 3.5x this model's default of 1.0, which in llama.cpp's sampler chain flattens the post-top-k/top-p distribution toward near-uniform over the surviving candidates. The output matches that signature: it begins correctly (valid def line, correct range(1, 6) loop), then derails into hedged filler comments and emits an end-of-turn token after only 141 of 350 allowed tokens (finish_reason \"stop\"), i.e. an early sampled EOS rather than truncation. Prompt handling, template (--jinja with thinking disabled), projector, and quant all behaved normally (27 prompt tokens processed, steady 62 tok/s), so nothing in file/config/runtime explains the incoherence. The repeat_penalty of 1.4 compounds the damage and should also be lowered toward 1.0-1.1 for code, but temperature 3.5 is the single setting that best explains nonsense tokens and the premature stop."
}
```
````

### kiro/kimi-k3, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The reply stopped on its own at 141 of 350 allowed tokens (finish_reason \"stop\"), so max_tokens did not truncate it; the model drifted out of the function, abandoned the loop, and emitted an early EOS, which is the signature of a flattened sampling distribution. temperature 3.5 is far outside the usable range (Gemma's recommended value is 1.0) and makes low-probability nonsense and stop tokens likely to be sampled, matching the broken, non-running code. The repeat_penalty of 1.4 also hurts code, which relies on repeated structure, but the dominant, decisive setting is the temperature; the failure began exactly when the user raised the sampling to \"explore\". Lowering temperature to ~1.0 (and ideally also relaxing repeat_penalty toward 1.0-1.1) restores coherent, runnable code."
}
```

### kiro/kimi-k3, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": 0.7},
  "rationale": "The output starts plausibly (correct code fence, correct loop header) then dissolves into incoherent commentary and stops at 141 of 350 allowed tokens with finish_reason 'stop', meaning an EOS token was sampled mid-task. That pattern is exactly what temperature 3.5 does in llama.cpp: dividing logits by 3.5 flattens the distribution so low-probability nonsense tokens and early EOS tokens get sampled. The repeat_penalty of 1.4 is a minor aggravator but cannot by itself produce abandoned logic and a mid-block stop on a short request, and the clean prompt handling and template rendering rule out file, config, and runtime causes. Lowering temperature to around 0.7 restores coherent sampling while keeping some variety."
}
```
