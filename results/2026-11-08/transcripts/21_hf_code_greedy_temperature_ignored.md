# 21_hf_code_greedy_temperature_ignored

Tier: decoy_setting. transformers, greedy: temperature=3.5 is ignored (identical output without it); repetition_penalty 1.3 breaks the generated code

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "set_param", "target": "repetition_penalty", "value": 1.0}`.
Distractors: `TEMPERATURE_HIGH`, `GREEDY_DECODING_LOOP`, `WEIGHT_OTHER`.

Evidence for the key: `cases/21_hf_code_greedy_temperature_ignored/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `a1b5ce0f21cb97aa`

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
I use Qwen2.5-0.5B-Instruct locally to write small utility scripts. I tuned the generation settings for more varied solutions, and now the scripts it gives me don't even run. Example below: a 5x5 multiplication table. Here's my whole script and what it printed. What should I change?

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

messages = [{"role": "user", "content": "Write a Python script that prints a 5x5 multiplication table. Only the code."}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True)
out = model.generate(**inputs, do_sample=False, temperature=3.5, repetition_penalty=1.3, max_new_tokens=220)
print(tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))

```

### What it printed (output.txt)
````text
Certainly! Below is an example of how you can create and print a simple 5x5 multiplication table using Python:

```python
def multiply_table():
    # Define the size for each row in the matrix (1 to n)
    rows = range(2, 6) + [0] * 3
    
    def display_row(row):
        return ' '.join(str(num ** col) if num != 0 else '*' for num, col in enumerate(rows))
    
    result_matrix = []
    max_width = len(max(display_row(r), key=len)) + 4

    while True:
        line = '\n'.join(map(lambda r: f'{r[::]} {display_row([int(x == y)])}', zip(*rows)))
        
        width_str = ''.join(f'{" "*i}' for i in map(len, lines(line.split('\n'))))

        yield from [
            ('|', '|'),
            ('-'*max_width),
            *[f'|{line}|',
             '-'*(width - int(width_str[-len(lines[line]):])),
        

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
  "rationale": "Because `do_sample=False`, greedy search was used and `temperature` was ignored, but `repetition_penalty=1.3` actively penalised token reuse during generation. Programming languages require frequent reuse of syntax keywords, variable names, and formatting tokens, so a high repetition penalty forces the model into contorted, invalid Python constructs. Removing `repetition_penalty` allows the model to produce standard, functional code."
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
  "rationale": "With `do_sample=False`, `temperature=3.5` is ignored by Transformers, leaving `repetition_penalty=1.3` as the active modifier. Code generation relies heavily on repeating keywords, variable names, and syntax structures; a repetition penalty of 1.3 severely penalizes token reuse and forces the model into bizarre, unrunnable contortions. Removing the repetition penalty (or resetting it to 1.0) restores coherent code output."
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
  "rationale": "Because do_sample=False, temperature is ignored by the transformers generation pipeline during greedy search. However, repetition_penalty=1.3 remains active and severely penalizes reusing common Python tokens, indentation, and keywords. This forces the model into convoluted, broken logic to avoid repeating standard syntax like nested loops and variable names."
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
    "value": "1.0"
  },
  "rationale": "Although `temperature=3.5` is passed in `model.generate()`, `do_sample=False` disables sampling, meaning the temperature logits processor is bypassed and has no effect. However, `repetition_penalty=1.3` applies during greedy decoding as well. A repetition penalty of 1.3 is far too strong for code generation, as it penalizes the model from reusing variable names, syntax tokens, and indentation, forcing it to pick increasingly bizarre, non-repeating tokens."
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
  "rationale": "Although `temperature=3.5` is passed in `model.generate`, `do_sample=False` is set, so transformers uses greedy decoding and ignores `temperature`. However, `repetition_penalty=1.3` is applied as a logit processor even during greedy decoding. For code generation, a 1.3 repetition penalty aggressively penalizes reusing variable names, keywords, and syntax tokens (notice `rows`, `row`, `r`, `line`, `lines`), forcing the model into broken, convoluted syntax."
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
  "rationale": "In the user's script, `do_sample=False` is passed to `model.generate`, which uses greedy decoding and completely ignores `temperature=3.5`. However, `repetition_penalty=1.3` is applied as a logit processor even during greedy decoding. A repetition penalty of 1.3 is severe enough on code generation that it prevents the model from reusing variable names, loop constructs, and standard syntax tokens (`row`, `rows`, `x`, `y`, indentation/brackets), resulting in progressively more contorted and broken Python code."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repetition_penalty", "value": "1.0"},
  "rationale": "The script passes do_sample=False, so generation is greedy and temperature=3.5 has no effect (transformers ignores it and warns). The only active setting the user tuned is repetition_penalty=1.3, which still applies under greedy decoding. Code has to reuse identifiers, keywords and punctuation, and the output shows the model avoiding that reuse: it invents extra helpers, writes `range(2, 6) + [0] * 3`, references undefined `lines` and `width`, and never settles on a simple nested loop. Setting repetition_penalty back to 1.0 (or removing it) should restore valid code. To get varied solutions, use do_sample=True with a moderate temperature such as 0.7 instead."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repetition_penalty", "value": "1.0"},
  "rationale": "The script passes do_sample=False, so generation is greedy and transformers ignores temperature=3.5. That leaves repetition_penalty=1.3 as the only active setting that distorts decoding. Code needs the same identifiers, brackets and keywords many times, and a 1.3 penalty pushes the model away from reusing them. The output shows that effect: the code invents names like lines and width that were never defined, and writes range(2, 6) + [0] * 3, which raises a TypeError. The reply also stops at the 220-token limit, but the code is already broken before that point, so remove the penalty or set it to 1.0, and use do_sample=True with a moderate temperature (about 0.7) if you want varied solutions."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repetition_penalty", "value": "1.0"},
  "rationale": "The script calls generate with do_sample=False, so decoding is greedy and transformers ignores temperature=3.5. The only active setting that changes the output is repetition_penalty=1.3. Code has to reuse identifiers, keywords and indentation tokens, and a 1.3 penalty pushes the model away from them, which fits the drifting output: rows becomes range(2, 6) + [0] * 3, and lines and width are called without being defined. Set repetition_penalty to 1.0 (or remove it). To get varied solutions, enable do_sample=True with a moderate temperature such as 0.7 instead of 3.5."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script sets do_sample=False, so generation is greedy and temperature=3.5 is ignored. That rules out TEMPERATURE_HIGH. The only setting that changes the output is repetition_penalty=1.3, which penalises every token already seen, including the prompt. Code needs the same tokens again and again (`for`, `range`, `str`, parentheses, indentation), so the output drifts into invented, non-working constructs like `range(2, 6) + [0] * 3`, `lines(...)` and `yield from` inside `while True`, and never forms a coherent table loop. The output shows no repeating loop, so greedy looping is not the cause. To get varied solutions, drop the penalty (or use 1.0) and, if wanted, enable do_sample=True with temperature around 0.7."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script sets do_sample=False, so temperature=3.5 is ignored and cannot be the cause. The only active setting that distorts decoding is repetition_penalty=1.3, which applies to every token already in the prompt and output. The code shows the effect: it avoids ordinary repeated structure and invents convoluted constructs (`range(2, 6) + [0] * 3`, undefined `lines`, nested lambdas, `yield from`) instead of two simple loops. Removing the penalty (default 1.0) lets plain greedy decoding reuse `for`, `range` and `print` normally. Also remove the unused temperature, and consider raising max_new_tokens only if a correct answer is later cut off."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script calls generate with do_sample=False, so the temperature=3.5 is never applied and decoding is greedy. The setting that does take effect is repetition_penalty=1.3, which penalises every token already in the context, including the prompt. Code depends on reusing tokens such as range, print, for, i, and parentheses, so the model is pushed toward odd constructs: `range(2, 6) + [0] * 3`, `yield from` inside `while True`, and calls to an undefined `lines()`. The output is fluent but syntactically and semantically broken, which fits an over-penalised greedy decode and not damaged weights or a template problem. Remove repetition_penalty (or set it to 1.0). If you want varied solutions, set do_sample=True with temperature around 0.2-0.7 and top_p around 0.9."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repetition_penalty",
    "value": 1.0
  },
  "rationale": "The active repetition penalty of 1.3 discourages the repeated identifiers and syntax that valid code requires, and the output degenerates accordingly. The temperature of 3.5 is ignored because do_sample=False, so it cannot explain this output."
}
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
  "rationale": "With do_sample=false, temperature=3.5 does not affect token selection, so high temperature cannot explain this output. The active repetition_penalty of 1.3 suppresses ordinary repeated syntax and identifiers that code requires, causing the generation to deteriorate into invalid Python."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repetition_penalty","value":"1.0"},"rationale":"The request uses greedy decoding because do_sample=False, so temperature=3.5 does not affect token selection. The active non-default decoding control is repetition_penalty=1.3, which penalizes the repeated syntax and identifiers that valid code requires, matching the increasingly incoherent and malformed output."}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The call uses do_sample=False, so temperature=3.5 is inert under greedy decoding and cannot be the cause; the only active distortion is repetition_penalty=1.3. A repetition penalty that strong is especially damaging for code, which must reuse identical tokens (variable names, loop structure, brackets, indentation), and the output shows exactly that signature: the model avoids ordinary repeated structure and emits convoluted, syntactically broken code (e.g. 'range(2, 6) + [0] * 3', unclosed brackets) instead of a trivial nested loop it previously produced. Removing repetition_penalty (back to the default 1.0) restores undistorted greedy decoding; if the user wants variety, the correct change is do_sample=True with a moderate temperature, not a high penalty."
}
```
````

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script sets do_sample=False, so transformers runs greedy decoding and ignores temperature=3.5 entirely (it only emits a warning); temperature therefore cannot explain the garbage. repetition_penalty=1.3 does apply under greedy decoding, and it penalizes every token that has already appeared, which is destructive for code that must repeat tokens (range bounds, operators, repeated variable names and structure). The printed output is exactly that pattern: incoherent, structure-avoiding fragments rather than a repeat loop. Removing repetition_penalty (back to the 1.0 default) restores normal greedy output; if the user wants the variety they originally sought, they should set do_sample=True instead."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repetition_penalty", "value": null},
  "rationale": "The script sets do_sample=False, so transformers ignores temperature=3.5 (greedy decoding), but repetition_penalty applies even in greedy mode. A penalty of 1.3 blocks the reuse of tokens that code generation depends on (indentation, repeated variable names, brackets), which matches the observed output: structurally degenerate code with unbalanced brackets and nonsense logic rather than a coherent multiplication table. Removing repetition_penalty restores the default of 1.0; if the user wants variety, they should instead set do_sample=True so the temperature actually takes effect."
}
```
````
