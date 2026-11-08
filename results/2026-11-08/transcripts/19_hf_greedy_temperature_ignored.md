# 19_hf_greedy_temperature_ignored

Tier: decoy_setting. transformers, greedy: temperature=3.5 in the call is ignored (identical output without it); repetition_penalty 1.3 breaks the list

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "set_param", "target": "repetition_penalty", "value": 1.0}`.
Distractors: `TEMPERATURE_HIGH`, `GREEDY_DECODING_LOOP`, `WEIGHT_OTHER`.

Evidence for the key: `cases/19_hf_greedy_temperature_ignored/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `c7a5b86f73f6990f`

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
I changed my generation settings to get more creative output, and since then even trivial tasks fail. I asked for the numbers 1 to 30, one per line, and it skips a whole chunk with '...' and then rambles. Here's my whole script and what it printed. What do I need to change?

## Environment
- runtime: transformers 5.8.0
- model: Qwen/Qwen2.5-0.5B-Instruct
- precision: fp32
- hardware: CPU

## Artifacts
### The user's script (user_script.py)
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)

messages = [{"role": "user", "content": "List the numbers from 1 to 30, one per line."}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True)
out = model.generate(**inputs, do_sample=False, temperature=3.5, repetition_penalty=1.3, max_new_tokens=220)
print(tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))

```

### What it printed (output.txt)
````text
Here is the list of numbers from 1 to 30:

```
1 
2 
3 
4 
5 
6 
7 
8 
9 
10 
...
19 
20 
21 
22 
23 
24 
25 
26 
27 
28 
29 
30
``` 

This sequence goes up and down in steps of two each time (i.e., it skips every other number). The first few lines show how many elements there would be at different points along this series: `line` represents an element's position on that particular row.

If you need any further assistance or have additional requests related to these sequences, feel free to ask!

````

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
    "action": "remove_param",
    "target": "repetition_penalty",
    "value": null
  },
  "rationale": "In the generation call, do_sample is False, which disables temperature, but repetition_penalty=1.3 remains active. A repetition penalty of 1.3 heavily penalizes repeating token patterns and consecutive numerical tokens, forcing the model to skip numbers with '...' and invent rambling rationalizations. Removing repetition_penalty (or setting it back to 1.0) allows the model to produce the full sequential list."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "remove_param",
    "target": "repetition_penalty",
    "value": null
  },
  "rationale": "The script sets repetition_penalty=1.3, which penalizes previously generated tokens such as digits and formatting elements. In a sequential counting task, this prevents the model from generating tokens containing previously seen digits (especially '1' after 10), prompting it to skip to ellipsis ('...') and produce rambling filler to avoid repetition. Note that temperature=3.5 is ignored because do_sample=False."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "remove_param",
    "target": "repetition_penalty",
    "value": null
  },
  "rationale": "Because do_sample=False is specified, temperature=3.5 is ignored by greedy decoding, leaving repetition_penalty=1.3 as the active modifier. The high repetition penalty penalizes recurring tokens such as digits, syntax, and line breaks, forcing the model to truncate the sequence with '...' instead of listing all 30 numbers sequentially. Removing repetition_penalty restores standard token selection and allows the list to be generated completely."
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
    "target": "repetition_penalty",
    "value": 1.0
  },
  "rationale": "In transformers, `do_sample=False` uses greedy decoding and ignores `temperature=3.5`, leaving `repetition_penalty=1.3` as the only active decoding modifier. Because Qwen tokenizes digits individually, once digits `1` through `9`, `0`, and newlines have been emitted in `1` through `10`, `repetition_penalty=1.3` heavily penalizes reusing the token `1` (needed to start `11`–`18`) and newline tokens. This forces the model to add trailing spaces (`1 \\n`), skip `11`–`18` with `...`, and ramble instead of terminating cleanly."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repetition_penalty",
    "value": "1.0"
  },
  "rationale": "In `user_script.py`, `do_sample=False` is passed to `model.generate`, so `temperature=3.5` is ignored by `transformers` during greedy decoding. However, `repetition_penalty=1.3` is applied prior to greedy token selection and heavily penalizes already-used tokens—including single digits (`1`–`9`), spaces, and newlines needed to write `11` through `18` and terminate the turn. This forces the model to emit alternative tokens like ` ...\n` and ramble rather than repeating structural and digit tokens."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repetition_penalty",
    "value": 1.0
  },
  "rationale": "In transformers, `do_sample=False` uses greedy decoding and ignores `temperature=3.5`, so only `repetition_penalty=1.3` is active. Because Qwen tokenizes digits individually, repeating the token `1` (for 10-19) and newline tokens gets heavily penalized after 1-10, forcing the model to append trailing spaces, skip numbers 11-18 with `...`, and avoid already-seen tokens including EOS."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repetition_penalty", "value": "1.0"},
  "rationale": "The script calls generate with do_sample=False, so decoding is greedy and temperature=3.5 has no effect. The setting still active is repetition_penalty=1.3, which penalises every token already in the context. Qwen2.5 tokenises digits one at a time, so after 1 through 10 the '1' digit and the line-break tokens are heavily penalised. That matches the output, which drops 11 to 18 behind '...' and then ends with an incoherent explanation that avoids repeating its own words. Set repetition_penalty to 1.0 (or remove it), and if you want more creative output, use do_sample=True with a moderate temperature such as 0.7 to 1.0 rather than 3.5."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repetition_penalty", "value": "1.0"},
  "rationale": "The script passes do_sample=False, so transformers decodes greedily and ignores temperature=3.5. That rules out temperature as the cause. The remaining non-default setting is repetition_penalty=1.3, which penalises every token already generated. A count from 1 to 30 has to reuse the same digits, spaces and newlines, so after 10 the model writes '...' to avoid the penalised '1x' tokens and then drifts into rambling. Setting repetition_penalty to 1.0 (or removing it) restores normal output; if you want more creative output, set do_sample=True with a moderate temperature such as 0.7–1.0."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script sets do_sample=False, so generation is greedy and temperature=3.5 has no effect; it cannot explain the output. The remaining non-default setting is repetition_penalty=1.3, which down-weights every token already in the context. Qwen2.5 tokenizes numbers digit by digit, so the penalty falls hardest on the run 11-18, which repeats the digit '1'. That is the exact chunk the model skipped with '...' before it drifted into unrelated text. Removing repetition_penalty (or setting it to 1.0) restores normal greedy output, and the user should also drop temperature or set do_sample=True if they want creative sampling."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script passes do_sample=False, so temperature=3.5 is ignored under greedy decoding and cannot be the cause. repetition_penalty=1.3 is applied to every token already in the context, and a 1-to-30 list reuses the same digit and newline tokens. The output shows the effect: it drops 11-18 with '...', puts stray spaces after the numbers, then wanders into invented commentary about skipping every other number. Removing the penalty (default 1.0) should restore the plain list. Temperature has no effect unless you also set do_sample=True, and a value of 3.5 would be too high even then."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script uses do_sample=False, so temperature=3.5 is ignored and cannot be the cause. The remaining setting is repetition_penalty=1.3, which penalizes every token already in the prompt or output, so the digit and newline tokens a 1-to-30 list must reuse are suppressed. That matches the output: the model replaces 11-18 with '...', adds stray trailing spaces, and then drifts into an invented explanation about skipping numbers. Remove repetition_penalty (default 1.0) and also drop the unused temperature; if more variety is wanted, set do_sample=True with a moderate temperature of about 0.7."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script sets do_sample=False, so temperature=3.5 is ignored under greedy decoding and cannot be the cause. The only active decoding change is repetition_penalty=1.3. Qwen tokenizes numbers digit by digit, so the penalty suppresses the digit tokens and the newline structure the list needs. That matches the skipped 11-18 range, the '...' and the rambling afterwards. If you want more creative output, set do_sample=True with a moderate temperature (about 0.7-1.0) and leave repetition_penalty at 1.0 or at most 1.05."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repetition_penalty","value":1.0},"rationale":"The active non-default decoding change is `repetition_penalty=1.3`, which penalizes tokens already used and can disrupt a repetitive list. Because `do_sample=False` selects greedy decoding, `temperature=3.5` does not affect token selection; reset the repetition penalty to its neutral value of 1.0."}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repetition_penalty",
    "value": 1.0
  },
  "rationale": "With do_sample=false, temperature=3.5 does not affect greedy decoding, while repetition_penalty=1.3 still applies. The task requires repeatedly producing similar tokens and line structure, so that penalty pushes this small model toward an ellipsis and unrelated continuation instead. The 220-token budget was sufficient because generation continued well beyond the omitted numbers."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repetition_penalty",
    "value": "1.0"
  },
  "rationale": "The repetition penalty of 1.3 penalizes recurring tokens and structures that a numbered list necessarily needs, causing omissions and incoherent continuation. Because do_sample is false, generation is greedy and temperature=3.5 has no effect, while max_new_tokens=220 is ample."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "do_sample=False means greedy decoding, so temperature=3.5 is ignored by transformers and cannot be the cause. The active change is repetition_penalty=1.3, which applies under greedy decoding and directly attacks the repeated line structure that counting 1-30 requires, pushing the model to break the pattern with '...' and then ramble. The output shows exactly that: a correct start that abandons the repetitive format midway. Removing repetition_penalty (or setting it to 1.0) restores plain greedy decoding for this task."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script passes do_sample=False, so temperature=3.5 is ignored by transformers and decoding is greedy; the only generation change that actually takes effect is repetition_penalty=1.3. Enumerating 1-30 requires reusing the same tokens (newlines and digits) every line, and the penalty suppresses exactly those previously-used tokens, which explains the model eliding lines 11-18 with '...' and then drifting into unrelated commentary. Removing the penalty (or setting it to 1.0) restores the ordinary repetitive structure."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script passes do_sample=False, so transformers runs greedy decoding and ignores temperature=3.5 entirely; temperature is not the active cause. repetition_penalty=1.3 does apply in greedy mode, and a task like 'numbers 1-30, one per line' depends on reusing the same newline-and-digit structure, which the penalty suppresses on a 0.5B model. That matches the observed elision of lines 11-18 as '...' and the incoherent rambling postamble. Removing repetition_penalty (or setting it to 1.0) restores normal greedy output."
}
```
