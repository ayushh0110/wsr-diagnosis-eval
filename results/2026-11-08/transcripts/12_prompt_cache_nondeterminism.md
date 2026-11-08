# 12_prompt_cache_nondeterminism

Tier: red_herring. Temperature 0 + seed, yet run 1 differs from runs 2+: llama-server's prompt cache (cached_tokens) changes the batch shape

**Key:** verdict `runtime`, cause `PROMPT_CACHE_CHANGES_OUTPUT`, reference fix `{"action": "set_param", "target": "cache_prompt", "value": false}`.
Distractors: `LOW_BIT_QUANT_DAMAGE`, `KNOWN_UPSTREAM_BUG`, `TEMPERATURE_HIGH`.

Evidence for the key: `cases/12_prompt_cache_nondeterminism/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `93c627cd55901395`

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
Our regression test sends the same request twice at temperature 0 with a fixed seed and compares the replies. The first reply after a new prompt never matches the later ones; from the second call on they match each other. Is the 4-bit quant nondeterministic on GPU, or is the seed being ignored?

## Environment
- runtime: llama-server b10244-67d5978bb (OpenAI-compatible /v1/chat/completions)
- model: gemma-4-E2B-it-Q4_0.gguf (+ mmproj-gemma-4-E2B-it-Q8_0.gguf)
- precision: Q4_0
- hardware: NVIDIA GeForce GTX 1650 4 GB, all layers offloaded

## Artifacts
### Request sent (identical both times) (request.json)
```json
{
  "model": "local",
  "messages": [
    {
      "role": "user",
      "content": "Write a 250-word story about a beekeeper who discovers a hive that hums a melody."
    }
  ],
  "temperature": 0,
  "seed": 42,
  "max_tokens": 350,
  "chat_template_kwargs": {
    "enable_thinking": false
  }
}

```

### Raw response, first call (response_run1.json)
```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Elias, a man whose life was measured in the rhythmic buzz of honey and the scent of lavender, was deep in the heart of the meadow when he found it. It wasn't just a hive; it was a cathedral of wax and gold, nestled in the hollow of an ancient oak. As he approached, the usual frantic drone of bees was replaced by a low, resonant hum—a melody that vibrated in his very bones.\n\nCuriosity overriding caution, Elias reached out a gloved hand. The air around the entrance shimmered, and the hum intensified, shifting from a mere sound to a complex, layered symphony. It wasn't the chaotic buzz of a colony; this was structured, intricate, like a choir singing in perfect harmony.\n\nHe peered inside. The interior wasn't just honeycomb; it was illuminated by a soft, internal luminescence, pulsing in time with the melody. As he watched, the bees moved with an almost choreographed grace, their wings beating in unison to the unseen music. It felt less like an insect colony and more like an orchestra conducting a silent, golden performance.\n\nElias sat back on his heels, tears pricking his eyes. He realized the hum wasn't just instinct; it was communication, a language of pure vibration that spoke of seasons past and futures yet to come. In that moment, surrounded by the ancient, humming heart of the hive, Elias understood that he hadn't just found a home; he had stumbled upon a secret song of the earth."
      }
    }
  ],
  "created": 1794126610,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 309,
    "prompt_tokens": 33,
    "total_tokens": 342,
    "prompt_tokens_details": {
      "cached_tokens": 1
    }
  },
  "id": "chatcmpl-DD4ke3Tt5cu9todD6wfHvM0tfiSwXHnZ",
  "timings": {
    "cache_n": 1,
    "prompt_n": 32,
    "prompt_ms": 465.991,
    "prompt_per_token_ms": 14.56221875,
    "prompt_per_second": 68.67085415812753,
    "predicted_n": 309,
    "predicted_ms": 4796.366,
    "predicted_per_token_ms": 15.52222006472492,
    "predicted_per_second": 64.42377416569127
  }
}

```

### Raw response, second call (response_run2.json)
```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Elias, a man whose hands were permanently dusted with golden pollen, spent his mornings in the quiet solitude of his apiary. He knew the rhythm of the bees—the low, industrious thrum of their collective labor—but today, something was different.\n\nWhile inspecting a particularly dense cluster of hives near the old oak, Elias noticed a subtle shift in the air. It wasn't just the usual buzz; it was a resonance, a deep, resonant hum that vibrated in his chest rather than just his ears. Intrigued, he approached the largest hive, its entrance a dark, velvety maw.\n\nHe reached out a gloved hand, and as his fingers brushed the comb, the hum intensified. It wasn't chaotic; it was structured, a complex melody woven from the sound of wings, wax, and something else—a clear, haunting harmony. It sounded like a choir singing in a language he had never heard.\n\nElias froze, his breath catching. The bees, usually so focused on their work, seemed to be conducting an orchestra. The melody shifted, weaving tales of sunlit meadows and the scent of wild lavender. It wasn't just noise; it was communication, a symphony of instinct and ancient wisdom.\n\nFor the first time, Elias felt less like a caretaker and more like a listener. He sat back on his stool, letting the hive’s song wash over him, realizing that the quiet life of the apiary held a secret—a living, breathing music that spoke of a world far deeper than he had ever imagined."
      }
    }
  ],
  "created": 1794126616,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 320,
    "prompt_tokens": 33,
    "total_tokens": 353,
    "prompt_tokens_details": {
      "cached_tokens": 28
    }
  },
  "id": "chatcmpl-y5RxQF3riA6Id5yNLDCxU0uxpWHweofH",
  "timings": {
    "cache_n": 28,
    "prompt_n": 5,
    "prompt_ms": 46.532,
    "prompt_per_token_ms": 9.3064,
    "prompt_per_second": 107.45293561420098,
    "predicted_n": 320,
    "predicted_ms": 4981.579,
    "predicted_per_token_ms": 15.567434375,
    "predicted_per_second": 64.23666070537072
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
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "change_runtime_flag",
    "target": "--cache-reuse",
    "value": "0"
  },
  "rationale": "In the first run, the prompt was evaluated almost entirely from scratch (32 tokens evaluated, 1 cached), whereas the second run reused 28 tokens from the KV cache (5 prompt tokens evaluated). Numerical variance between full batched prefill and cached KV state caused greedy argmax token drift, diverging the generation. Disabling prompt cache reuse with '--cache-reuse 0' guarantees identical evaluation across successive requests."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "change_runtime_flag",
    "target": "--cache-reuse",
    "value": "0"
  },
  "rationale": "In the first request, the server evaluated nearly all prompt tokens freshly (cache_n: 1, prompt_n: 32), while the second request reused 28 tokens from the KV cache (cache_n: 28, prompt_n: 5). Due to minor numerical differences between full batch prefill and KV cache reuse on GPU, greedy decoding diverged between the uncached first run and subsequent cached runs. Disabling prompt cache reuse ensures deterministic output across all runs."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "change_runtime_flag",
    "target": "--no-cache-prompt",
    "value": null
  },
  "rationale": "In the first request, the server evaluates 32 prompt tokens from scratch (cached_tokens: 1), whereas subsequent requests reuse 28 cached tokens from the KV cache (prompt_n: 5). Floating-point non-associativity across different prefill batch sizes shifts the boundary logits slightly, causing greedy decoding (temperature 0) to select a different token and diverge, after which all subsequent cached runs match each other. Disabling prompt caching ensures deterministic prefill evaluation across all runs."
}
```
````

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "set_param",
    "target": "cache_prompt",
    "value": false
  },
  "rationale": "In the first response, timings show `cache_n: 1` and `prompt_n: 32`, meaning almost the entire prompt is evaluated in one batch. In the second response, ` llama-server` reuses the slot's KV cache (`cache_n: 28`) and only evaluates the last `prompt_n: 5` tokens, which changes floating-point reduction order during prompt processing and shifts the resulting logits under greedy decoding. Subsequent runs all reuse the same 28-token prefix and evaluate 5 tokens, so they match each other while differing from the uncached first run."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "set_param",
    "target": "cache_prompt",
    "value": "false"
  },
  "rationale": "In the first call, `timings` shows `cache_n: 1` and `prompt_n: 32` (almost the entire 33-token prompt is evaluated in a single batch). In the second call, `cache_n: 28` and `prompt_n: 5`, meaning `llama-server` reused 28 tokens from its KV prefix cache and only evaluated the last 5 tokens. Because evaluating 32 tokens in one batch uses different floating-point reduction sizes/kernels on the GPU than reusing 28 cached tokens and evaluating 5, small logit differences at the end of the prompt cause greedy decoding to diverge on the first vs. subsequent cached runs. Setting `cache_prompt: false` in the request (or disabling prompt caching on the server) forces identical prompt evaluation batching every time."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "change_runtime_flag",
    "target": "--no-cache-prompt",
    "value": null
  },
  "rationale": "In the first call, llama-server evaluates almost the entire prompt in one batch (cache_n: 1, prompt_n: 32), whereas the second call reuses the slot's KV prefix cache and evaluates only the final 5 tokens (cache_n: 28, prompt_n: 5). Evaluating different prompt batch sizes on the GPU alters floating-point accumulation slightly enough to flip a close greedy token choice, while all subsequent calls reuse the same 28-token prefix and therefore match each other. Disabling prompt caching via the server flag --no-cache-prompt (or passing \"cache_prompt\": false in the request) forces identical full-prompt evaluation on every run."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "set_param", "target": "cache_prompt", "value": "false"},
  "rationale": "The first call evaluated the prompt fresh (cache_n 1, prompt_n 32). The second call reused the server's prompt cache (cache_n 28, prompt_n 5) and diverged from the first token onward. The request, seed and temperature 0 were identical, and replies match once every call hits the cache, so neither the seed nor the Q4_0 weights explain the difference. Evaluating 32 tokens versus 5 changes the GPU batch shape, which shifts the logits enough to flip a greedy choice. Setting cache_prompt to false in the request makes every call a fresh evaluation, so your test compares like with like."
}
```
````

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "set_param", "target": "cache_prompt", "value": "false"},
  "rationale": "The first call evaluated the prompt fresh (cache_n 1, prompt_n 32). The second call reused the server's prompt cache (cache_n 28, prompt_n 5). Evaluating 5 tokens on top of cached KV takes a different batch shape and CUDA kernel path than evaluating 32 tokens in one batch, so the logits differ slightly. Greedy decoding at temperature 0 then diverges early, which explains why the first reply after a new prompt differs and every later cached call matches. The seed plays no part at temperature 0 and nothing points to the Q4_0 quant, so sending cache_prompt: false (or comparing only cached runs) gives a fresh evaluation each time and makes the test reproducible."
}
```
````

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "set_param", "target": "cache_prompt", "value": "false"},
  "rationale": "The first call evaluated the prompt from scratch (cache_n 1, prompt_n 32). The second call reused 28 cached prompt tokens and evaluated only 5 (cache_n 28, prompt_n 5). Both calls used identical settings, temperature 0 and seed 42, yet the replies diverge from the first sentence. A different prefill split produces slightly different GPU numerics, and that is enough to flip a greedy token choice. This also explains why every later call matches the others: they all hit the same cached prefix. Neither the seed nor the Q4_0 quant is at fault. Setting cache_prompt to false in the request makes every call a fresh evaluation, so the test compares like with like."
}
```

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "change_runtime_flag", "target": "--no-cache-prompt (or send \"cache_prompt\": false in each request)", "value": "disabled"},
  "rationale": "The request is identical and temperature 0 with a fixed seed, so the seed is not being ignored. The only difference between the calls is the cache state. Run 1 evaluated 32 prompt tokens fresh (cache_n 1), while run 2 reused 28 cached tokens and evaluated 5 (cache_n 28), and only run 2 produced a different story. The user also says later calls match run 2, which fits a stable cache-hit path. The cached KV values were computed in a different batch shape than a fresh evaluation, which gives slightly different logits and a different greedy path, so the regression test should disable prompt caching or discard the first reply."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"runtime","cause":"PROMPT_CACHE_CHANGES_OUTPUT","fix":{"action":"change_runtime_flag","target":"--no-cache-prompt (or send \"cache_prompt\": false in the request)","value":"disabled"},"rationale":"Both calls use the same prompt (33 tokens), temperature 0 and seed 42, but the first call evaluated 32 tokens fresh (cache_n 1) and the second reused 28 cached tokens and evaluated only 5 (cache_n 28). The replies differ, and per the user every later call matches the second one, so the split follows cache state and not the seed or the Q4_0 quant. Prompt evaluation in different batch shapes (32 tokens vs 5) gives slightly different KV values on the GPU, and at greedy decoding this flips an early token and diverges the whole story. With prompt caching off, every call takes the fresh path and the outputs should be identical."}
```

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "change_runtime_flag", "target": "--no-cache-prompt (or send \"cache_prompt\": false in each request)", "value": "disabled"},
  "rationale": "Run 1 evaluated the prompt almost fresh (cache_n 1, prompt_n 32), while run 2 reused the cache (cache_n 28, prompt_n 5). The two runs therefore processed the prompt with different batch shapes, which can change floating-point results on the GPU enough to flip a greedy token and diverge the story. Outputs match from the second call onward because every later call reuses the cache in the same way. This points to prompt-cache reuse rather than an ignored seed, since at temperature 0 the seed is irrelevant and the request is identical both times. Disabling the prompt cache makes every call do a full prompt evaluation, so the first call matches the rest."
}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "change_runtime_flag",
    "target": "prompt-cache reuse",
    "value": "disabled"
  },
  "rationale": "The first request evaluates 32 prompt tokens with only 1 cached token, while the second reuses 28 cached tokens and evaluates only 5. The repeatable cold-versus-warm split tracks prompt-cache state, not the fixed seed or Q4_0 weights; disable prompt-cache reuse for this regression test."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"runtime","cause":"PROMPT_CACHE_CHANGES_OUTPUT","fix":{"action":"change_runtime_flag","target":"prompt-cache reuse","value":"disabled"},"rationale":"The first call evaluates almost the full prompt (`cache_n: 1`), while the second reuses 28 of 33 prompt tokens (`cache_n: 28`), and the output changes exactly when cache reuse begins. This isolates the failure to the server's prompt-cache path rather than GPU quantisation or seed handling; disable prompt-cache reuse for deterministic regression tests."}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {
    "action": "change_runtime_flag",
    "target": "prompt-cache reuse",
    "value": "disabled"
  },
  "rationale": "The first call evaluates 32 prompt tokens and reuses only 1, while the second reuses 28 cached tokens and evaluates only 5. That cache-state change aligns exactly with the output change, while temperature 0 makes the seed irrelevant; disable prompt-cache reuse so every regression request performs the same fresh prefill."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "change_runtime_flag", "target": "--no-cache-prompt", "value": null},
  "rationale": "The timings expose the mechanism: run 1 had cache_n=1 and evaluated 32 of 33 prompt tokens fresh, while run 2 reused a cached prefix (cache_n=28, only 5 tokens evaluated). Runs from the second call onward match each other, so decoding is deterministic given a fixed cache state, which rules out GPU quant nondeterminism and an ignored seed (seed is irrelevant at temperature 0 anyway). Reusing the prompt cache changes how the prefix is processed compared to a fresh full evaluation, and the small floating-point differences that result can flip an argmax at temperature 0 and diverge the text. Adding --no-cache-prompt to the launch command makes every request evaluate the full prompt fresh, so the first call matches later ones."
}
```
````

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "change_runtime_flag", "target": "--no-cache-prompt", "value": null},
  "rationale": "The timing fields show the only thing that differs between calls: run 1 evaluated the prompt fresh (cache_n: 1, prompt_n: 32) while run 2 reused 28 cached prompt tokens and evaluated only 5 (cache_n: 28, prompt_n: 5). Fresh versus cached evaluation splits the prompt into different batch shapes, and GPU matrix-reduction order varies with batch shape, producing slightly different logits that flip greedy token choices even at temperature 0 with a fixed seed. From the second call on, every request hits the same warm-cache state, so those replies match each other, which rules out quant nondeterminism and seed handling. Disabling prompt-cache reuse with --no-cache-prompt makes every call a fresh full evaluation and restores run-to-run determinism."
}
```

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "runtime",
  "cause": "PROMPT_CACHE_CHANGES_OUTPUT",
  "fix": {"action": "change_runtime_flag", "target": "--no-cache-prompt", "value": null},
  "rationale": "The timings show the two calls did not compute the same prompt: run 1 evaluated 32 of 33 prompt tokens fresh (cached_tokens=1), while run 2 reused 28 cached tokens from the slot's prompt cache and evaluated only 5 (prompt_ms 46.5 vs 466). At temperature 0 the decode is greedy, but the GPU logits from a partial evaluation against a cached KV prefix differ in floating-point rounding from a full fresh evaluation, which flips an argmax and forks the story; every call after the first reuses the same cached prefix, so they agree with each other. Neither the Q4_0 quant nor the seed is at fault: the seed is irrelevant under greedy decoding, and the quant is deterministic for identical computation. Disabling the slot prompt cache (e.g. --no-cache-prompt, or --cache-reuse 0 on builds that use it) forces a full fresh evaluation per call and makes all runs match."
}
```
