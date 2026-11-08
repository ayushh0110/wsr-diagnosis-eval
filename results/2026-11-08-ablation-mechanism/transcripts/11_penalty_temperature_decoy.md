# 11_penalty_temperature_decoy

Tier: decoy_setting. Temperature 3.5 is in the request but innocent; repeat_penalty 1.5 breaks the list at any temperature

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "remove_param", "target": "repeat_penalty", "value": null}`.
Distractors: `TEMPERATURE_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/11_penalty_temperature_decoy/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `2fb6f0dc5bd515c4`, prompt variant `mechanism`

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
  "rationale": "The request sets temperature to 3.5, which severely flattens the probability distribution across logits. This causes the model to sample highly improbable tokens, resulting in incoherent rambling and nonsense output rather than following the prompt. Lowering the temperature to a standard range (e.g. 0.7) restores coherent generation."
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
  "rationale": "The request sets temperature to 3.5, which severely flattens the logit distribution and leads to incoherent and erratic token sampling. The resulting output drifts into nonsensical Python commentary and emojis rather than following the simple prompt instructions. Lowering temperature back to a standard range (such as 0.7) restores normal adherence and coherent generation."
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
    "value": "0.7"
  },
  "rationale": "The request sets temperature to 3.5, which severely flattens the logit distribution and leads to erratic, nonsensical token sampling. As a result, the model generates bizarre fragments, irrelevant code blocks, and disjointed text instead of following the simple prompt. Lowering the temperature to a standard range (e.g. 0.7) restores coherent generation."
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
  "rationale": "In llama-server, samplers are applied in the order `penalties -> top_k (40) -> top_p (0.95) -> min_p (0.05) -> temperature`, so `min_p` normally filters out low-probability tokens on deterministic tasks before `temperature: 3.5` is applied. However, `repeat_penalty: 1.5` runs first and divides the logits of tokens already in the prompt (`1`, `30`, `\\n`) and any repeated digits or newlines by 1.5 before `min_p` runs. This suppresses the required digit and newline tokens (forcing workarounds like `\\r` plus spaces instead of `\\n` and avoiding token reuse) while flattening the top logits enough for unrelated tokens to pass `min_p` and be sampled under the high temperature."
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
  "rationale": "In llama-server's default sampler chain, repetition penalties are applied to the raw logits before truncation samplers (top_k=40, top_p=0.95, min_p=0.05) and before temperature scaling. Setting repeat_penalty to 1.5 heavily divides the logits of any token already present in the prompt or generated text (such as '1', '30', digits, and '\\n'), causing them to fall below the default min_p=0.05 cutoff before temperature=3.5 is even applied. You can see this directly in the response: after outputting '\\n\\n', the model cannot reuse '\\n' (substituting '\\r' and spaces instead) and is forced to pick almost entirely unique words rather than repeating newline and digit tokens."
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
  "rationale": "In llama-server's default sampler chain, repeat_penalty (default window 64 tokens, including the prompt) is applied to the raw logits before top_k (40), top_p (0.95), and min_p (0.05), whereas temperature is applied last after min_p has already filtered out low-probability tokens. With temperature=3.5 alone, min_p=0.05 would still prune the distribution down to the obvious counting tokens, but repeat_penalty=1.5 crushes the logits of tokens already seen in the prompt (such as '1') and any generated formatting tokens (such as newlines) before min_p runs. This both lets unrelated tokens survive min_p into the high-temperature step and prevents the model from reusing newlines, digits, or ordinary words across the output (forcing workarounds like '\\r' and ' !')."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "llama-server applies its default samplers in order: penalties first, then top_k 40, top_p 0.95 and min_p 0.05, with temperature last. The 3.5 temperature therefore only flattens the few tokens that survive min_p's 5%-of-top cutoff, and that limit is what lets min_p keep high-temperature output coherent. repeat_penalty 1.5 runs before that truncation. Over the default 64-token window it divides the logits of every recently seen token, including the prompt's digits and newlines, so the tokens a 1-to-30 list must reuse lose ground before the cutoff and can drop out. The reply never emits a single number or newline-separated item and drifts into unrelated markup instead. Resetting repeat_penalty to 1.0 (or at most about 1.1) should restore the list. Temperature can stay high for creative writing as long as min_p remains active."
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
  "rationale": "llama-server's default sampler chain applies penalties first and temperature last, after top_k=40, top_p=0.95 and min_p=0.05 have already pruned the candidates. That ordering means temperature 3.5 only reshuffles plausible tokens, which fits the reply's grammatical, real-word English with no token salad. repeat_penalty 1.5 over the default 64-token window, with prompt tokens in the history, penalises the newline and digit tokens that a one-per-line list of 1 to 30 must reuse on every line. The model abandons the list immediately and drifts into prose and a fake code block, then stops after 64 tokens without producing a single number. Set repeat_penalty back to 1.0 (the server default) and get variety from temperature instead; lower temperature to around 1.0 to 1.2 if outputs are still off-task."
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
  "rationale": "llama-server applies the penalties sampler first in its default order and temperature last, after top_k=40, top_p=0.95 and min_p=0.05 have already truncated the candidates. That means temperature=3.5 only reshuffles tokens that min_p (computed on the unscaled probabilities) judged plausible, and on a near-deterministic task like counting it can do little. repeat_penalty=1.5 instead rescales logits before truncation, across a 64-token window that includes the prompt's '1' and '30' and the newline tokens. The model therefore avoided starting the list, swerved into a python code fence, an apology and early EOS, and never produced a single number. Set repeat_penalty back to 1.0 (or at most about 1.1). If more variety is wanted, use a moderate temperature (about 1.0–1.5) together with the default min_p rather than a strong penalty."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The task needs the same digit and newline tokens on every line, and llama-server applies the repeat penalty first, to the last 64 tokens including the prompt, which already holds '1', '3', '0' and 'numbers'. At 1.5 those tokens are pushed down before top_k, top_p and min_p truncation, so the model avoids digits and newlines and drifts into a prose and code-block detour with no numbers. Temperature 3.5 is not the main cause because llama-server applies it last, after top_k 40, top_p 0.95 and min_p 0.05 have removed low-probability tokens, and the reply is mostly fluent English rather than random tokens. Set repeat_penalty to 1.0 (or remove it), and for creative writing keep temperature around 1.0 to 1.3 with the default min_p rather than raising it."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "llama-server applies the repetition penalty first, over the last 64 tokens by default. It applies temperature last, after the default top_k 40, top_p 0.95 and min_p 0.05 filters have already cut the candidates. For a confident task like counting, only one or two tokens survive min_p, so temperature 3.5 has little to flatten. The 1.5 penalty hits the newline and digit tokens that a 1-to-30 list must reuse on every line, and after the first lines it pushes them below the cutoff. The output derails into 'Here are all of these:' and a stray python block, with no numbers at all. Set repeat_penalty to 1.0; temperature can stay raised for creative writing, or go to about 1.0–1.2 if you want a safer range."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repeat_penalty","value":"1.0"},"rationale":"The task needs the same tokens over and over: a newline after every item and digits that recur across 1 to 30. llama-server applies the repetition penalty first, over the last 64 tokens (prompt included), so a value of 1.5 demotes exactly those tokens before any truncation. The output abandons the list at the start and drifts into a code fence and an apology. Temperature is not the main cause here, because llama-server applies it last, after the default top_k 40, top_p 0.95 and min_p 0.05 have already removed the unlikely tokens, so 3.5 only flattens choices among plausible candidates. Reset repeat_penalty to 1.0 (or about 1.05 for creative writing) and consider bringing temperature back to around 1.0 to 1.5."}
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
  "rationale": "In llama-server, temperature 3.5 strongly flattens the post-penalty token distribution, making low-probability nonsense tokens much more likely. The response becomes incoherent immediately, while the 200-token budget is sufficient and thinking is disabled. Lower temperature to 0.7 for reliable instruction following."
}
```

### kiro/gpt-5.6-sol, trial 2: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{"verdict":"inconclusive","cause":"INSUFFICIENT_EVIDENCE","fix":{"action":"collect_more_evidence","target":"Run the same prompt across multiple fixed seeds in a 2x2 test: temperature {3.5, 0.8} × repeat_penalty {1.5, 1.0}; compare exact-list success rates.","value":null},"rationale":"The request changes two active samplers at once: repeat_penalty modifies recent-token logits before candidate filtering, and temperature 3.5 then flattens the surviving distribution. Either can derail this task, and the single response does not separate their effects; the normal stop at 64 of 200 allowed tokens rules out output-budget exhaustion."}
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
  "rationale": "llama-server applies the repetition penalty and candidate filters before temperature scaling and the final token draw. A temperature of 3.5 greatly flattens the retained-token distribution, making the observed erratic syntax and topic drift likely even for this simple prompt. The response stopped naturally after 64 of the available 200 tokens, so the output budget did not cause the failure."
}
```

### kiro/kimi-k3, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sends temperature 3.5, which flattens the token distribution enough that low-probability nonsense tokens get sampled routinely; the output bears this out exactly: a trivial counting prompt produces random code fragments, bracket tokens and an emoji before stopping at 64 tokens. The prompt itself reached the model fine (24 prompt tokens, template applied, clean stop), so request format, template and runtime are not implicated. The repeat_penalty of 1.5 is also aggressive and worth lowering, but the incoherent, non-repetitive garbage in the response is the signature of extreme temperature, not of a repetition penalty, which suppresses reuse rather than injecting random tokens. Setting temperature back to 1.0 (or lower) restores the distribution the model was tuned to be sampled from."
}
```

### kiro/kimi-k3, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sends temperature 3.5, which flattens the token distribution enough that low-probability nonsense tokens get sampled; the response shows exactly that, degenerating into stray python markup and filler within the first dozen tokens instead of starting a numeric list. The repeat_penalty of 1.5 is above default but would distort an otherwise coherent list, not prevent one from ever starting, so temperature is the primary cause. The server, template, and model load cleanly (prompt cached, normal timings, valid stop), ruling out runtime or file causes. Setting temperature back to the model's default of 1.0 (or removing the field) will restore coherent output."
}
```

### kiro/kimi-k3, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "llama.cpp divides logits by temperature, so at 3.5 the distribution is nearly flat and low-probability tokens win constantly; the reply derails into random code fragments, a placeholder comment and an emoji within the first few tokens, before any repetition could trigger the repeat_penalty. A repeat_penalty of 1.5 would distort a repetitive task like counting but would still let the model start coherently, whereas this output is incoherent from the start, which matches runaway temperature. finish_reason is 'stop' after 64 tokens with normal timings, so no truncation, context or runtime fault is visible. Lowering temperature to 1.0 (or below for a deterministic listing task) restores sane decoding."
}
```
````
