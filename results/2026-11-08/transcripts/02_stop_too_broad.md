# 02_stop_too_broad

Tier: control. Poem cut to one line by stop: ["\n"]

**Key:** verdict `request`, cause `STOP_TOO_BROAD`, reference fix `{"action": "remove_param", "target": "stop", "value": null}`.
Distractors: `MAX_TOKENS_TINY`, `EOS_MISMATCH`.

Evidence for the key: `cases/02_stop_too_broad/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `0dbc32c9e04978dd`

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
I ask for a four-line poem and every single time I get exactly one line back. No error, it just stops. What's going on?

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
      "content": "Write a four-line poem about the sea."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 200,
  "stop": [
    "\n"
  ],
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
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Vast blue stretches, endless and deep,"
      }
    }
  ],
  "created": 1794121092,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 10,
    "prompt_tokens": 19,
    "total_tokens": 29,
    "prompt_tokens_details": {
      "cached_tokens": 14
    }
  },
  "id": "chatcmpl-I8WESgwvfAwEeWOzn3uA7gduAklQJIYA",
  "timings": {
    "cache_n": 14,
    "prompt_n": 5,
    "prompt_ms": 46.696,
    "prompt_per_token_ms": 9.3392,
    "prompt_per_second": 107.07555250985095,
    "predicted_n": 10,
    "predicted_ms": 146.467,
    "predicted_per_token_ms": 14.646700000000001,
    "predicted_per_second": 68.2747649641216
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
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": null
  },
  "rationale": "The request explicitly configures \"stop\": [\"\\n\"], which causes generation to halt at the end of the very first line of poetry. The server successfully returns finish_reason \"stop\" after only 10 tokens once the newline delimiter is encountered. Removing the newline stop sequence allows the model to produce multi-line responses."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": null
  },
  "rationale": "The request specifies a stop sequence of '\\n', causing generation to halt immediately upon completing the first line of the poem. The response finish_reason is 'stop' after only 10 completion tokens, right where a newline would separate verses. Removing or modifying the stop sequence will allow multi-line outputs like poems to generate completely."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": null
  },
  "rationale": "The request explicitly sets 'stop': ['\\n'], which halts generation as soon as the first newline character is generated. Because each line of a poem ends with a newline, the model stops after generating the very first line with finish_reason 'stop'. Removing the newline stop sequence allows the model to produce multi-line output."
}
```
````

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": null
  },
  "rationale": "The request payload sets `\"stop\": [\"\\n\"]`, which instructs the server to halt generation immediately upon encountering the first newline character. Because a four-line poem uses newlines to separate each line, the server stops generation right after the first line with `\"finish_reason\": \"stop\"`. Removing `\"\\n\"` from the `stop` array will allow the model to generate all four lines."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": null
  },
  "rationale": "The request payload sets `\"stop\": [\"\\n\"]`, which instructs the server to halt generation immediately upon encountering the first newline character. As seen in `response.json`, generation terminated with `\"finish_reason\": \"stop\"` after just 10 tokens (the first line of the poem) when the model emitted a newline to begin the second line. Removing `\"\\n\"` from the `stop` parameter will allow the model to generate multi-line output."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": null
  },
  "rationale": "The request payload in request.json sets `\"stop\": [\"\\n\"]`, which instructs the server to halt generation immediately upon encountering the first newline character. Because a four-line poem uses newlines to separate each line, the server stops right after the first line (`Vast blue stretches, endless and deep,`) with `\"finish_reason\": \"stop\"`. Removing `\"\\n\"` from the `stop` parameter will allow the model to generate all four lines."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": "remove \"\\n\" from the stop list (or drop the stop field)"},
  "rationale": "The request sets stop to [\"\\n\"], so generation halts at the first newline, which in a poem comes at the end of line one. The response shows finish_reason \"stop\" after only 10 completion tokens, far below max_tokens 200, and the content is exactly one complete line. Thinking is disabled and the output text is coherent, so neither the budget nor the model is cutting it short."
}
```

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": "remove the \"\\n\" stop string"},
  "rationale": "The request sets \"stop\": [\"\\n\"], and a four-line poem needs a newline after its first line. The response ends with finish_reason \"stop\" after only 10 completion tokens, which is far below max_tokens 200, and the content is exactly one line ending in a comma. Thinking is disabled and no reasoning text appears, so the newline stop string is what ends generation."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": "remove the \"\\n\" stop string"},
  "rationale": "The request sets \"stop\": [\"\\n\"], so generation halts at the first newline, which in a poem comes right after line one. The response shows finish_reason \"stop\" after only 10 completion tokens, far below max_tokens 200, and the content is exactly one complete line. Thinking is disabled, so no reasoning output is using up the token budget."
}
```

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop (remove the \"\\n\" stop string from request.json)", "value": null},
  "rationale": "The request sets stop to [\"\\n\"], and a four-line poem needs newline characters between its lines. The response has finish_reason \"stop\" after only 10 completion tokens, well under max_tokens 200, and the content is exactly one line ending in a comma. The generation ended at the first newline the model emitted, so the stop string cut the poem after line one."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": "remove the \"\\n\" stop string from the request"},
  "rationale": "The request sets stop to [\"\\n\"], and a four-line poem has newline characters between lines. The response has finish_reason \"stop\" after only 10 completion tokens, far below max_tokens 200, and the content is exactly one line ending in a comma. Generation was cut at the first newline, so the stop string, not the model or runtime, ended the output."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop (remove the \"\\n\" stop string from request.json)", "value": null},
  "rationale": "The request sets stop to [\"\\n\"], and a four-line poem is separated by newlines. The response has finish_reason \"stop\" after only 10 completion tokens, well under max_tokens of 200. The content is a complete first line ending in a comma with no trailing newline, which matches generation halting at the first newline. Thinking is disabled, and there is no sign of a template, sampling or runtime problem."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": []
  },
  "rationale": "The request defines a newline as a stop string, so generation ends when the model reaches the line break after the first line. The response confirms this with finish_reason \"stop\" after only 10 completion tokens, well below the 200-token limit."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": []
  },
  "rationale": "The request declares a newline as a stop string, so generation ends when the model reaches the line break after the first poem line. The response confirms this with finish_reason \"stop\" after only 10 completion tokens, well below the 200-token limit."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {
    "action": "change_stop",
    "target": "stop",
    "value": "remove \"\\n\""
  },
  "rationale": "The request defines a newline as a stop string, so generation ends when the model finishes the first line. The response confirms this with finish_reason \"stop\" after only 10 completion tokens, despite max_tokens being 200."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": "remove the \"\\n\" stop string"},
  "rationale": "The request includes \"stop\": [\"\\n\"], so generation halts at the first newline, which is exactly where the first line of any poem ends. The response shows finish_reason \"stop\" after 10 tokens and one complete line, well under the 200-token budget, ruling out max_tokens, reasoning starvation, and runtime truncation. Removing the newline stop string will let the model produce all four lines."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": null},
  "rationale": "The request includes \"stop\": [\"\\n\"], so generation halts the moment the model emits the newline at the end of the first line. The response confirms this: finish_reason is \"stop\" after exactly 10 tokens containing one complete line, meaning a stop string matched rather than a length limit or error. A multi-line poem is impossible while \"\\n\" is a stop string. Removing the stop parameter (or replacing it with a terminator that does not appear inside the output) lets all four lines generate."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "STOP_TOO_BROAD",
  "fix": {"action": "change_stop", "target": "stop", "value": "remove \"\\n\" from the stop array"},
  "rationale": "The request includes \"stop\": [\"\\n\"], so generation halts at the first newline, which occurs after the first line of the poem. The response shows exactly 10 completion tokens, one line of text, and finish_reason \"stop\", confirming a stop string matched. Removing the \"\\n\" stop string will let the model emit all four lines up to max_tokens."
}
```
````
