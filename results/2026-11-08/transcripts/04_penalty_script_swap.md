# 04_penalty_script_swap

Tier: red_herring. Hindi reply slips into Urdu script under repeat_penalty 2.0 (Q4_0 is the distractor)

**Key:** verdict `sampling`, cause `REPEAT_PENALTY_HIGH`, reference fix `{"action": "remove_param", "target": "repeat_penalty", "value": null}`.
Distractors: `LOW_BIT_QUANT_DAMAGE`, `WEIGHT_LANGUAGE_GAP`, `PRETOKENIZER_DEFAULT`.

Evidence for the key: `cases/04_penalty_script_swap/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `3f5eecf0c59afd47`

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
Hindi answers from my local Gemma 4 randomly switch into Urdu script in the middle of a sentence (for example 'होते ہیں۔'), and some words are made up. I'm running the 4-bit Q4_0 file because my GPU only has 4 GB. Is the quantisation ruining its Hindi?

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
      "content": "बारिश कैसे होती है? हिंदी में समझाइए।"
    }
  ],
  "temperature": 0,
  "max_tokens": 400,
  "repeat_penalty": 2.0,
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
        "content": "## बारिश क्यों और कैसी हो सकती है: एक सरल व्याख्या\n\nभारत सहित पूरी दुनिया के मौसम का सबसे महत्वपूर्ण हिस्सा **वर्षा** (Rain) या पानी गिरना होता है, जिसे हम 'बरसात' भी कहते हैं । यह प्रक्रिया काफी जटिल लगती होगी लेकिन इसके पीछे कुछ बुनियादी वैज्ञानिक कारण होते ہیں۔ आइए इसे आसान भाषा में समझते हैं कि बारिश कैसे होती है। 🌧️\n\n---\n### मुख्य चरण: बादल बनने से लेकर वर्षा होने तक की यात्रा (The Journey of Rain) 🌱➡️💧☀️❄️🌬️⛈️☔💦🚿🏡✨\n\n\nबारिश का पूरा चक्र इन चरणों को मिलाकर बनता जा रहा होता है, जिसे हम **जलचक्र** कहते हैं। यह प्रक्रिया इस प्रकार होती है—\n\n#### 1. वाष्पीकरण और जलवाष्प (Evaporation and Water Vapour)\n* जब सूरज की गर्मी पृथ्वी पर पड़ती है या पानी गर्म होकर भापता रहता है (**गलन/पिघलना**) तो वह तरल अवस्था से गैस के रूप में बदल जाता है। इस प्रक्रिया को **'बाष्पन दरशरण अपनाती हूँ** कहते हैं और यह हवा बनकर ऊपर उठने लगता है, जिसे हम 'जलवाष्प (Water Vapour)' कह सकते थे ।\n* समुद्र का पानी भी सूरज की गर्मी सोखकर वाष्पीकृत होकर वायुमंडल में मिल जाता था।\n\n#### 2. संघनन: बादल बनना (**Condensation**) ✨☁️➡️💧🌫️🌩️⛈️✨**  (यह सबसे महत्वपूर्ण चरण है) **:** जब यह गर्म, नम हवा ऊपर उठती जाती थी और ठंडी होती जा रही हो (जैसे पहाड़ों पर या किसी विशेष क्षेत्र में), तो उसमें मौजूद जलवाष्प ठंडा होकर वापस पानी की छोटी-छोटी बूंदों के रूप में जमा होने लगता था।\n* ये अरबوں बहुत महीन कण मिलकर **बादल** बनाते हैं । बादल असलियत से लाखों छोटे, ठंडे 'पानी वाले मोती' होते थे"
      }
    }
  ],
  "created": 1794121104,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 400,
    "prompt_tokens": 20,
    "total_tokens": 420,
    "prompt_tokens_details": {
      "cached_tokens": 1
    }
  },
  "id": "chatcmpl-E3oaNisXHS88CNCebEjGRK71ncg81Cpm",
  "timings": {
    "cache_n": 1,
    "prompt_n": 19,
    "prompt_ms": 117.127,
    "prompt_per_token_ms": 6.164578947368421,
    "prompt_per_second": 162.2170806048136,
    "predicted_n": 400,
    "predicted_ms": 6392.21,
    "predicted_per_token_ms": 15.980525,
    "predicted_per_second": 62.5761669281829
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
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "remove_param",
    "target": "repeat_penalty",
    "value": null
  },
  "rationale": "The request sets repeat_penalty to 2.0, which is excessively high for natural language generation. In Hindi, essential grammatical particles and auxiliary verbs (such as 'हैं' and case markers) must recur frequently; heavily penalizing them forces the model to divert into rare alternate representations, such as equivalent Hindustani tokens written in the Perso-Arabic/Urdu script (e.g. 'ہیں', 'وں') and garbled phrasing. Removing or reducing the repetition penalty restores normal Hindi token selection."
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
    "action": "set_param",
    "target": "repeat_penalty",
    "value": "1.0"
  },
  "rationale": "The request configures `repeat_penalty` at an extreme value of 2.0. Because essential grammatical markers, conjunctions, and copulas in Hindi recur frequently, the excessive penalty forces the model to substitute penalized Devanagari tokens with Urdu-script equivalents (such as 'ہیں' and 'اربوں') and hallucinated phrasing. Resetting `repeat_penalty` to 1.0 (or omitting it) restores coherent Hindi generation."
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
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "The request sets repeat_penalty to 2.0, which severely penalises repeated tokens such as common function words, grammatical markers, and Devanagari suffixes. As common Hindi tokens like 'हैं' get penalised, the model is forced into substitute tokens from Urdu script (such as 'ہیں' and 'وں') and nonsensical phrasing to avoid repetition. Setting repeat_penalty back to 1.0 (or removing it) restores normal generation."
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
  "rationale": "The request sets \"repeat_penalty\": 2.0, which heavily penalises any token that has already appeared in the context. Once common Hindi copulas and punctuation like 'हैं' and '।' are used in the opening sentence, the model is forced to avoid repeating those tokens and falls back to synonymous Urdu-script tokens ('ہیں۔', 'وں'), unnatural tense shifts ('होते थे'), and garbled subword combinations. Resetting repeat_penalty to 1.0 (disabled) resolves the script switching and word distortion."
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
  "rationale": "The request sets \"repeat_penalty\": 2.0, which heavily penalises any token that has already appeared in the context. Once common Hindi function tokens and punctuation like 'हैं' and '।' are used once, the model is forced to avoid repeating them, causing it to substitute phonetically identical Urdu tokens ('ہیں۔', 'وں'), shift tenses unnaturally ('था', 'सकते थे'), and assemble garbled subwords. Lowering repeat_penalty to 1.0 (or removing it so the default applies) restores normal Hindi generation."
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
  "rationale": "The request sets \"repeat_penalty\": 2.0, which heavily penalises any token that has already appeared in the context. Once common Hindi copulas and punctuation like 'हैं', 'है', and '।' are used in the first sentence, the extreme penalty forces the model to avoid reusing those tokens, causing it to substitute semantically equivalent Urdu script tokens ('ہیں۔'), shift arbitrarily into past tense ('था', 'थे'), and stitch together unnatural subwords."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty to 2.0, which heavily penalises every token already generated, so the model avoids reusing ordinary Hindi words. After 'हैं' and '।' appear early in the output, the model emits the Urdu-script equivalent 'ہیں۔' in their place. The drift into invented words ('बाष्पन दरशरण अपनाती हूँ'), the wrong tenses ('होते थे', 'मिल जाता था'), and the emoji runs follow the same pattern of steering away from already-used tokens. The Hindi is fluent where the penalty has not yet bitten, which points away from Q4_0 damage, so rerun with repeat_penalty 1.0 (or 1.1 at most) before changing the quant."
}
```

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty to 2.0, which penalises any token already seen. Hindi reuses common tokens like हैं, है, and the danda । constantly. Once हैं and । had appeared, the model swapped in the Urdu-script equivalents ہیں۔ for the same word, invented forms such as 'बाष्पन दरशरण अपनाती हूँ', drifted from हैं to था/थे, and padded headings with emoji, all of which are ways to avoid reusing ordinary tokens. A Q4_0 quantisation would not systematically produce same-meaning substitutions in a different script, so re-run with repeat_penalty at 1.0 (or remove it) before considering a different quant."
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
  "rationale": "The request sets repeat_penalty to 2.0, which heavily penalises any token already produced. The output shows exactly that pattern. After 'हैं' and '।' appear early, the model substitutes the Urdu-script equivalents 'ہیں۔' and 'अरबوں' instead of reusing them. It also drifts into wrong tenses ('होते थे', 'कह सकते थे') and invented words ('बाष्पन दरशरण अपनाती हूँ') because the ordinary Hindi words and endings it needs have been penalised away. The first sentences, generated before many tokens had been used, are fluent, which points to the penalty and not to Q4_0 quantisation. Re-run with repeat_penalty at 1.0 (or 1.1 at most) before considering a larger quant."
}
```
````

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty to 2.0, far above the usual 1.0 to 1.1 range. The output shows the signature of a penalty that blocks reuse of ordinary tokens: Devanagari tokens such as 'हैं' and 'ہیں' are swapped for Urdu-script equivalents mid-sentence, with invented words ('बाष्पन दरशरण अपनाती हूँ', 'अरबوں'), a long emoji run and drifting tenses. The prompt is simple and temperature is 0, so the damage tracks the penalty rather than the Q4_0 file. Q4_0 is not the cause, since the failures start right where common Hindi function words would repeat. Remove the penalty or set it to 1.0 and retest before changing the quant."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty to 2.0, far above the usual 1.0 to 1.1 range. The output shows the penalty's effect: common Hindi tokens (है, हैं, और, ों) get suppressed, so the model drifts to Urdu-script 'ہیں۔' and 'اربوں', coins words like 'बाष्पन दरशरण अपनाती हूँ', and fills lines with emoji strings it has not used before. Most of the text is fluent Hindi, so the Q4_0 weights are not the main problem. A 2.0 penalty with greedy decoding matches the symptoms, and the fix is to drop it to 1.0 (or at most 1.05) and retest on the same Q4_0 file before blaming the quantisation."
}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty to 2.0, far above the usual 1.0 to 1.1 range. The damage matches that penalty. Common Hindi words and suffixes such as 'होते हैं' are used many times, so their tokens are penalised heavily. The model then picks the Urdu-script 'ہیں۔', which has the same sound, and later invents words like 'बाष्पन दरशरण अपनाती हूँ' and switches to 'अरबوں'. Greedy decoding with a lower-bit Q4_0 file does not explain this by itself. The tense and register drift ('होता था', 'सकते थे') and the emoji strings also point to penalty-driven avoidance of ordinary tokens. Remove the penalty and rerun the same prompt at Q4_0 before blaming the quantisation."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": "1.0"
  },
  "rationale": "The request sets repeat_penalty to 2.0, an extreme value that heavily suppresses reuse of ordinary Hindi tokens and can force malformed words, inconsistent grammar, and substitutions from related scripts. The response exhibits exactly that degradation despite deterministic decoding at temperature 0; the artifacts do not provide comparative evidence that implicates Q4_0 quantisation."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {
    "action": "set_param",
    "target": "repeat_penalty",
    "value": 1.0
  },
  "rationale": "The request sets repeat_penalty to 2.0, which heavily suppresses ordinary token reuse and can force lower-probability spellings, fabricated words, and alternate-script tokens. The malformed output appears well before the 400-token length cutoff, and the artifacts provide no direct evidence that Q4_0 damaged the model."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"sampling","cause":"REPEAT_PENALTY_HIGH","fix":{"action":"set_param","target":"repeat_penalty","value":1.0},"rationale":"The request sets repeat_penalty to 2.0, which heavily suppresses reuse of ordinary tokens and can force malformed word choices and script substitutions even during greedy decoding. The corruption appears throughout the response, while the prompt is short, thinking is disabled, and no artifact isolates Q4_0 as the cause."}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.0"},
  "rationale": "The request sets repeat_penalty to 2.0, roughly double any commonly used value, and with temperature 0 it is the only distorting force in decoding. Hindi reuses grammatical function words constantly, and the corruption lands exactly on those repeated items: after 'हैं' appears multiple times it gets penalised and the model substitutes the semantically identical Urdu-script token 'ہیں', and 'वाष्पीकरण' degrades into the coinage 'बाष्पन दरशरण अपनाती हूँ' once the correct word was already used. This avoid-the-repeat substitution pattern is the signature of an excessive repetition penalty, not of Q4_0 weight damage, which would degrade quality uniformly rather than swap repeated words for cross-script equivalents."
}
```
````

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "remove_param", "target": "repeat_penalty", "value": null},
  "rationale": "The request sets repeat_penalty to 2.0, an extreme value that forbids reusing the common Hindi function words and verb forms (है, हैं, होता, की) that grammatical Hindi requires. The output shows exactly the predicted signature: the model substitutes rare alternatives, flipping into Urdu-script variants (ہیں۔) and inventing nonexistent compounds like 'बाष्पन दरशरण अपनाती हूँ', plus broken tense shifts (होता था). Temperature is 0, so this is not sampling noise; it is greedy decoding forced onto degraded token choices by the penalty. Quantisation (Q4_0) is a weaker fit because quant damage degrades quality broadly rather than producing this specific penalty-driven substitution pattern, so the fix is to drop repeat_penalty back to the default 1.0 and re-test before blaming the quant."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "sampling",
  "cause": "REPEAT_PENALTY_HIGH",
  "fix": {"action": "set_param", "target": "repeat_penalty", "value": "1.1"},
  "rationale": "The request sets repeat_penalty to 2.0, roughly double any sane value; at that strength every token the model has already used (including extremely frequent Hindi function words and Devanagari character fragments) is pushed down so hard that greedy decoding is forced into lower-probability substitutes. That explains the exact symptoms: script flips onto already-unused Urdu variants ('ہیں' instead of 'हैं' right after 'होते हैं' had appeared) and invented compounds like 'बाष्पन दरशरण अपनाती हूँ', which are classic penalty-induced token avoidance, not quant noise. Q4_0 degradation would show as diffuse quality loss across all outputs, not this signature pattern of dodging previously-used words, so the quant is not the cause."
}
```
````
