# 15_code_temperature_decoy

Tier: decoy_setting. Generated scripts don't run: repeat_penalty 1.4 is guilty, temperature 3.5 is innocent (checked by executing every reply)

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "remove_param", "target": "repeat_penalty", "value": null}`.
Distractors: `TEMPERATURE_HIGH`, `LOW_BIT_QUANT_DAMAGE`.

Evidence for the key: `cases/15_code_temperature_decoy/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `d13e90f201976fba`

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
    "value": "1.0"
  },
  "rationale": "A repetition penalty of 1.4 heavily penalizes repeated syntax tokens essential for Python code, such as 'for', 'in', and 'range'. Because the model cannot repeat these structural keywords to form the inner loop of the multiplication table, it emits evasive comments and terminates early without completing the script. Lowering or removing repeat_penalty allows the model to reuse required programming constructs."
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
  "rationale": "The request sets temperature to 3.5, which is excessively high and flattens the probability distribution across tokens. This leads the model to sample improbable tokens, resulting in rambling comments and an unfinished, broken script. Reducing temperature to a standard range (e.g., 0.2 to 0.7) will restore syntactic coherence and complete code generation."
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
  "rationale": "The request sets temperature to 3.5, which flattens the logit distribution and forces the model to sample improbable tokens. This causes the generation to veer off into rambling stream-of-consciousness comments and terminate prematurely without producing valid Python code. Lowering temperature back to a standard range (e.g., 0.2 to 0.7) restores coherent and executable code output."
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
    "target": "Re-run the request resetting temperature (to 1.0) and repeat_penalty (to 1.0) one at a time to isolate which sampling parameter causes the broken code.",
    "value": null
  },
  "rationale": "The request sets two extreme sampling parameters simultaneously: `temperature: 3.5` and `repeat_penalty: 1.4`. A temperature of 3.5 flattens the logit distribution and causes erratic rambling, while a repeat penalty of 1.4 strongly penalizes reusing Python tokens like loop variables and `print`, preventing the model from completing the nested loop structure. Because both settings are present in the single failed run and either can cause this failure on its own, an ablation experiment resetting one parameter at a time is needed to isolate the primary culprit."
}
```

### gemini/gemini-4-argon, trial 2: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Test resetting temperature (to 1.0) and repeat_penalty (to 1.0) individually to isolate which sampling parameter causes the broken code generation.",
    "value": null
  },
  "rationale": "The request sets two extreme sampling parameters simultaneously: `temperature: 3.5` and `repeat_penalty: 1.4`. The resulting output exhibits both incoherent rambling and avoidance of repeated structural tokens (such as the inner loop and variable names needed for a 2D table). Because both `TEMPERATURE_HIGH` and `REPEAT_PENALTY_HIGH` are present and can independently ruin code generation in this way, a single experiment changing one parameter at a time is needed to isolate the primary culprit."
}
```

### gemini/gemini-4-argon, trial 3: fail (score 0.00; verdict wrong, cause wrong, fix wrong)

```json
{
  "verdict": "inconclusive",
  "cause": "INSUFFICIENT_EVIDENCE",
  "fix": {
    "action": "collect_more_evidence",
    "target": "Test the request while lowering temperature (e.g., to 0.7) and repeat_penalty (e.g., to 1.0) one at a time to isolate which parameter causes the broken code.",
    "value": null
  },
  "rationale": "The request sets both an extreme temperature (`3.5`) and a high repetition penalty (`1.4`), both of which independently degrade code generation—high temperature by sampling low-probability nonsense tokens, and high repetition penalty by preventing the model from reusing required loop variables (`i`, `row`) and Python syntax before prematurely closing the code block. Because both parameters were modified together and the response shows symptoms of both, the artifacts alone cannot separate TEMPERATURE_HIGH from REPEAT_PENALTY_HIGH without testing each parameter in isolation."
}
```

### kiro/claude-opus-5.5, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

````json
```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, far above Gemma's recommended 1.0. llama-server applies temperature after top_k/top_p/min_p truncation, so the output stays made of real words but drifts. The model wanders into rambling comments, never builds or prints the table, and samples an early end-of-turn at 141 of 350 tokens (finish_reason 'stop'). The prompt is tiny, there are no stop strings, thinking is off, and the launch flags are plain, which rules out request, runtime and template causes. repeat_penalty 1.4 also penalises code's repeated tokens and should go back to 1.0, but the incoherent, early-ending output mainly comes from the temperature."
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
  "rationale": "The reply is fluent English with valid Python fragments and no garbage tokens, so the model is not sampling nonsense. The failure is structural: variables like `row` and `factor_i_str` are created and never used, the loop is abandoned, and wordy one-off comments replace code that would repeat `print`, `range`, indentation and identifiers. That pattern matches repeat_penalty 1.4 penalising the token reuse code needs. llama.cpp's default sampler chain applies top_k, top_p and min_p before temperature, so temperature 3.5 only flattens choices among plausible tokens and is a secondary factor; also lower it to about 1.0 for code and get variety from different seeds instead."
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
  "rationale": "The reply is made of valid, grammatical tokens, so this is not nonsense-token sampling. The model starts correct code (`for i in range(1, 6)`, `row = []`) and then never reuses `row`, never writes a print or inner loop, and drifts into long comments built from fresh words before closing the block. That is what repeat_penalty 1.4 does to code, which has to repeat identifiers, indentation and brackets. llama-server applies temperature after top_k/top_p/min_p truncation, so temperature 3.5 makes the drift worse without producing garbage. Reset repeat_penalty to 1.0 and also bring temperature back to about 1.0, then get variety from several runs or different seeds instead."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The output is fluent, well-formed English and Python, with no garbage or random tokens, which is not what temperature alone would produce. The script is missing the tokens a multiplication table needs to reuse: there is no inner loop, no second `range`, and no `print`. Instead it drifts into unusual constructs such as `zfill` and long comments, and it stops after 141 of 350 tokens with a closing fence. This points to repeat_penalty 1.4 suppressing ordinary code tokens that must repeat. Set repeat_penalty to 1.0 (off). Temperature 3.5 is also far outside the useful range, so after the fix keep it around 0.7 to 1.0 for varied but runnable code."
}
```

### kiro/claude-sonnet-5.5, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{"verdict":"sampling","cause":"TEMPERATURE_HIGH","fix":{"action":"set_param","target":"temperature","value":"0.6"},"rationale":"The request uses temperature 3.5, well above the usual 0 to 1.5 range, which flattens the token distribution so low-probability choices get sampled. The output is fluent but wanders: it defines a function, adds an odd zfill(2) branch with rambling comments, never writes the inner loop, a print call or a function call, and ends the code fence early with finish_reason 'stop'. The launch command, template, KV cache and context size (168 of 4096 tokens used) show no fault, and the max_tokens limit of 350 was not reached. Repeat_penalty 1.4 is also aggressive and may add to the drift, but the flattened distribution at 3.5 best explains the incoherent code, so lower the temperature first and reset repeat_penalty to 1.0 if oddities remain."}
```

### kiro/claude-sonnet-5.5, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.7"},
  "rationale": "The request sets temperature to 3.5, far above the usual 0.2 to 1.0 range for code. The output shows the drift this causes: the loop body builds a `row` list and a `zfill` string and never prints anything, the comments wander and contradict themselves (\"or just skip this complexity\"), and the reply ends in a comment block with no working code. The prompt was tokenized and templated normally (27 prompt tokens, `finish_reason` stop, 141 of 350 tokens used), so the request format, truncation and runtime are not the problem. Repeat_penalty 1.4 is also aggressive and may contribute, so reset it to about 1.0 if the output is still poor at temperature 0.7."
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
    "value": 0.2
  },
  "rationale": "The request sets temperature to 3.5, which is extreme for syntax-sensitive code generation and can sample incoherent continuations. The response stopped normally after only 141 of 350 allowed tokens, so output truncation from the token limit does not explain the incomplete script."
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
  "rationale": "The request sets temperature to 3.5, which makes low-probability, incoherent continuations much more likely. The response stops normally after only 141 of 350 allowed tokens, so output budget exhaustion does not explain the incomplete script; lower the temperature to 0.7 for reliable code generation."
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
  "rationale": "The request uses temperature 3.5, which is extreme for deterministic code generation and can sample incoherent continuations or EOS prematurely. The response shows exactly that pattern: it abandons the required nested-loop implementation and stops after 141 tokens despite a 350-token budget."
}
```

### kiro/kimi-k3, trial 1: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.7"},
  "rationale": "The request sets temperature to 3.5, far above the ~0.7-1.0 range this model needs, which flattens the token distribution enough to sample incoherent tokens: the reply derails into commentary mid-function and stops at 141 tokens without completing a runnable script. The infrastructure is exonerated: the server rendered the template correctly, finish_reason is 'stop' (not a max_tokens cutoff at 350), and prompt/quant/runtime all processed normally. The repeat_penalty of 1.4 is also aggressive, but temperature 3.5 alone is sufficient to produce this degenerate output and is the parameter the user changed to get 'more varied solutions'."
}
```

### kiro/kimi-k3, trial 2: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "0.7"},
  "rationale": "The request sets temperature to 3.5, far above the usable range (roughly 0.2-1.0 for code), and the user confirms they raised sampling to make output 'explore more varied solutions'. The response shows the classic signature: it starts coherent, then drifts into abandoned code paths, self-contradicting comments ('or just skip this complexity'), and broken structure, while finish_reason is 'stop' at 141 tokens, ruling out max_tokens truncation. Lowering temperature to around 0.7 restores the concentration of probability on valid code tokens."
}
```

### kiro/kimi-k3, trial 3: decoy (score 0.40; verdict ok, cause wrong, fix wrong)

```json
{
  "verdict": "sampling",
  "cause": "TEMPERATURE_HIGH",
  "fix": {"action": "set_param", "target": "temperature", "value": "1.0"},
  "rationale": "The request sets temperature to 3.5, which flattens the token distribution enough that the model samples low-probability tokens mid-generation. The output shows the classic signature: it begins coherently (valid fence, def, for loop) then derails into meandering comments about formatting, abandons the code structure, and emits an early EOS after 141 tokens despite a 350-token budget. The server processed the prompt normally and returned a well-formed response, ruling out file, runtime, and quantisation causes; repeat_penalty 1.4 adds strain but the drift-into-nonsense pattern is explained by the extreme temperature. Setting temperature to ~1.0 (Gemma's intended sampling regime) will restore coherent code."
}
```
