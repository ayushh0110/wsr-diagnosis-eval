# 03_image_field_ignored

Tier: control. Ollama-style images field sent to llama-server: the model never sees the picture

**Key:** verdict `request`, cause `IMAGE_FIELD_IGNORED`, reference fix `{"action": "change_request_format", "target": "messages[].content: [{type: text}, {type: image_url, image_url: {url: data:image/png;base64,...}}]", "value": null}`.
Distractors: `VISION_PROJECTOR_MISSING`, `WEIGHT_OTHER`.

Evidence for the key: `cases/03_image_field_ignored/answer.json` (provenance) and `evidence/`.

## Prompt (identical for every model and trial)

sha256 prefix `44384cd0f8039e30`

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
I'm sending a picture to my local Gemma 4 (it's a vision model) and it keeps replying that I haven't provided any picture. I've checked that the base64 is a valid PNG.

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
      "content": "What is in this picture? Describe it in two sentences.",
      "images": [
        "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAIAAABMXPacAAAB/klEQVR42u3cIVIDQRAF0KQrKodA47Gg0dgcIopjoCI4AoIboNGg0VjQaAQSqsJOhsx2876koKnptz3ZnQSW2/u3hYxLaAEAAAIAgAAAIAAACAAAcrystGBvbk4vvn/x+uWxS/Glw7hJfe8uAaC99V0YvAZ06H7zT5mAPk08ZBRMQM/uN9QB4Dmg0OXfUA1A5+5PrQnAFlTu8p9U2QSYAAD2n4H1TYAJACAAAAgAAP8uvd7XPaS+CTABAOxCAyvPAmC9OzMBg7s/0OAvhuD3NWM+134Zg0nVYlY7zz/ci2Ju+/4og15DMLXOmA9m7e3yx/Zpke1NgjbCmOc9T7rXg+YBOuoENLR1/qOQ5tPRzRf1QIM6fx9w4JYy3CD3XdDhG3rh29PIcsxQ1SASHfKUNIhcR2z1DCLdAWcxg8jYo0oGkbQ7ZQwib19qGETqjhQwWGVvxNevzvuoHDUuw7yjEGVWntQgKq05o0EUW206g6i3zlwGq14H9Jvd5ag13G0fPAcIAAACAIAAACAAAAiAhf8d/XN2H6+/+bbt+sQECAAAAgCAAAAgAAAIAAACAIAAACBdsnp+v+pSaDNuDb2WYAJsQQIAgBw1y/Pbc10wAQAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAAAEAAABAEAAABAAAKQxn+athyH8pBCxAAAAAElFTkSuQmCC"
      ]
    }
  ],
  "temperature": 0,
  "max_tokens": 200,
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
        "content": "Please provide the picture you are referring to. I need an image to be able to describe it for you."
      }
    }
  ],
  "created": 1794121095,
  "model": "~/.cache/huggingface/hub/models--ggml-org--gemma-4-E2B-it-GGUF/snapshots/b4243c156154b6dca9324415f8c7ccc098b4aed1/gemma-4-E2B-it-Q4_0.gguf",
  "system_fingerprint": "b10244-67d5978bb",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 23,
    "prompt_tokens": 21,
    "total_tokens": 44,
    "prompt_tokens_details": {
      "cached_tokens": 16
    }
  },
  "id": "chatcmpl-4DWqSiq0LbbnBJ9b5elwC7qzHjqGgmLy",
  "timings": {
    "cache_n": 16,
    "prompt_n": 5,
    "prompt_ms": 48.568,
    "prompt_per_token_ms": 9.7136,
    "prompt_per_second": 102.9484434195355,
    "predicted_n": 23,
    "predicted_ms": 345.352,
    "predicted_per_token_ms": 15.015304347826087,
    "predicted_per_second": 66.59871667168571
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
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": "array of parts with type text and image_url"
  },
  "rationale": "The raw response shows only 21 prompt tokens, meaning the image was never processed or passed to the model. llama-server's OpenAI-compatible /v1/chat/completions endpoint expects multimodal inputs formatted as a list of content parts with type 'image_url' (data URI or URL) rather than a separate 'images' array. Because the image was provided in an unsupported field, the server silently dropped it and processed only the text prompt."
}
```
````

### gemini/gemini-3.8-flash, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": null
  },
  "rationale": "The request places base64 image data into an Ollama-style 'images' array on the message object, which llama-server's OpenAI-compatible endpoint ignores. This is confirmed by the prompt token count of only 21 tokens, showing no image tokens were ingested. The image should be formatted within 'content' as structured parts using the standard OpenAI 'image_url' schema."
}
```
````

### gemini/gemini-3.8-flash, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "content",
    "value": null
  },
  "rationale": "The server's OpenAI-compatible `/v1/chat/completions` endpoint expects images inside the `content` list as `image_url` objects (e.g. data URLs), not in an Ollama-style top-level `images` array on the message. Because `images` was ignored, the prompt only evaluated 21 tokens (pure text without image embeddings), leading the model to accurately state that no image was provided."
}
```

### gemini/gemini-4-argon, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": "array of content parts using {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,...\"}}"
  },
  "rationale": "The request passes the base64 image inside an Ollama-style `images` array on the message object (`messages[0].images`), which llama-server's OpenAI-compatible `/v1/chat/completions` endpoint silently ignores. Because `content` is a plain string, only the 21 text tokens are evaluated (`prompt_tokens: 21`) and no image embeddings are injected despite `--mmproj` being loaded. Formatting `messages[0].content` as a multimodal array with `text` and `image_url` (data URI) parts allows `llama-server` to parse and encode the image."
}
```

### gemini/gemini-4-argon, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[0].content",
    "value": "OpenAI multimodal content array with type: image_url"
  },
  "rationale": "The server is running `llama-server` with the OpenAI-compatible `/v1/chat/completions` endpoint, which expects images to be passed inside the `content` array as `{\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,...\"}}` objects. Instead, the request passes an Ollama-style top-level `\"images\"` array alongside a string `\"content\"`, which `llama-server` silently ignores. This is confirmed by `prompt_tokens: 21` in the response usage, showing only the short text prompt was tokenized and no image tokens were evaluated."
}
```

### gemini/gemini-4-argon, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": "[{\"type\": \"text\", \"text\": \"...\"}, {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,...\"}}]"
  },
  "rationale": "The request sends the base64 image in a top-level `images` array on the user message (Ollama's native API format), which llama-server's OpenAI-compatible `/v1/chat/completions` endpoint silently ignores. Because the image field is not read, `usage.prompt_tokens` is only 21 tokens (the text prompt alone) even though `--mmproj` is loaded, causing the model to reply that no picture was provided. Sending the image inside `messages[].content` as an OpenAI `image_url` content part with a `data:image/png;base64,...` URI fixes the issue."
}
```

### kiro/claude-opus-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {"action": "change_request_format", "target": "messages[0].content", "value": "array of content parts: [{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<base64>\"}}]"},
  "rationale": "The request puts the image in a message-level \"images\" field, which is Ollama's native format; llama-server's OpenAI-compatible /v1/chat/completions only reads images from image_url content parts. The usage shows prompt_tokens = 21, only enough for the text prompt plus template tokens, so no image tokens were encoded. The server was launched with --mmproj, so the projector is loaded and is not the cause."
}
```

### kiro/claude-opus-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {"action": "change_request_format", "target": "messages[].content", "value": "[{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<base64>\"}}]"},
  "rationale": "The request puts the base64 PNG in a top-level \"images\" array on the message. That is Ollama's native format, and llama-server's OpenAI-compatible /v1/chat/completions does not read it. The usage block shows only 21 prompt tokens (16 cached, 5 evaluated), which is the text prompt alone with no image tokens, so the image was never encoded. The projector is loaded (--mmproj is in the launch command), so the model would see the image if it were sent as an image_url content part with a data: URI."
}
```

### kiro/claude-opus-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {"action": "change_request_format", "target": "messages[0].content", "value": "content array: [{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<data>\"}}]"},
  "rationale": "The request attaches the image in a top-level message field named \"images\". That is the Ollama-native shape. The OpenAI-compatible /v1/chat/completions endpoint in llama-server does not read it, and it expects image_url parts inside the content array. The response shows prompt_tokens of only 21, which is about the size of the text prompt plus template tokens, so no image embedding tokens were added. The server was launched with --mmproj, which rules out a missing projector, so the model simply never received the image."
}
```

### kiro/claude-sonnet-5.5, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[0].content",
    "value": "Make content an array of parts: [{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<BASE64>\"}}]. Remove the non-standard \"images\" field."
  },
  "rationale": "The request puts the image in a top-level \"images\" array on the message (an Ollama-style field), while content is a plain string. The /v1/chat/completions endpoint of llama-server reads images only from image_url content parts, so the field is ignored. The response shows usage.prompt_tokens of 21, which is just the text prompt with no image tokens, and the model answers that no picture was provided. The mmproj is loaded in the launch command, so the projector is not the problem."
}
```

### kiro/claude-sonnet-5.5, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"request","cause":"IMAGE_FIELD_IGNORED","fix":{"action":"change_request_format","target":"messages[0].content","value":"Send content as an array of parts: [{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<BASE64>\"}}], and remove the 'images' field from the message."},"rationale":"The request puts the PNG in an Ollama-style 'images' array on the message, a field llama-server's /v1/chat/completions does not read. It takes images only from 'image_url' content parts. prompt_tokens is 21 for a short text prompt, so no image tokens were added. The mmproj is passed on the launch command, so the projector is loaded, and the reply asking for a picture is the model reacting correctly to a prompt with no image."}
```

_2 attempts: the first reply did not parse; the final reply above is from the format retry._

### kiro/claude-sonnet-5.5, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{"verdict":"request","cause":"IMAGE_FIELD_IGNORED","fix":{"action":"change_request_format","target":"messages[0].content","value":"Make content an array of parts: [{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<BASE64>\"}}], and remove the non-standard top-level \"images\" field."},"rationale":"The request puts the PNG in a custom \"images\" array on the message (an Ollama-style field), while content is a plain string. llama-server's /v1/chat/completions only reads images from image_url parts inside a content array, so the field is ignored. The response confirms this: prompt_tokens is 21 (15 of them cached from the prior text-only request), which is far too few for a prompt that includes image embeddings, and the model says no image was provided. The mmproj is passed with --mmproj, so the projector is loaded and the launch command is not at fault."}
```

### kiro/gpt-5.6-sol, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": "Use an OpenAI multimodal content array containing a text part and an image_url part whose URL is data:image/png;base64,<base64-data>."
  },
  "rationale": "The request places the image in a sibling messages[].images field, which the OpenAI-compatible chat endpoint does not consume. The response reports only 21 prompt tokens, consistent with the server processing the text while omitting the image, even though the vision projector was supplied at launch."
}
```

### kiro/gpt-5.6-sol, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": "Use an OpenAI multimodal content array containing a text part and an image_url part whose URL is data:image/png;base64,<base64-data>."
  },
  "rationale": "The request places the image in a top-level messages[].images field, which the OpenAI-compatible chat endpoint does not consume. The response reports only 21 prompt tokens, consistent with processing the short text prompt without image tokens, even though the server was launched with a vision projector."
}
```

### kiro/gpt-5.6-sol, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {
    "action": "change_request_format",
    "target": "messages[].content",
    "value": "Use an OpenAI multimodal content array containing a text part and an image_url part whose URL is data:image/png;base64,<base64>; remove the top-level messages[].images field."
  },
  "rationale": "The request places the PNG in messages[].images, which the OpenAI-compatible chat endpoint does not consume as multimodal content. The 21-token prompt confirms that only the text was processed, while the launch command shows that a vision projector was supplied."
}
```

### kiro/kimi-k3, trial 1: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {"action": "change_request_format", "target": "messages[0].content", "value": "[{\"type\": \"text\", \"text\": \"What is in this picture? Describe it in two sentences.\"}, {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,<base64 PNG data>\"}}]"},
  "rationale": "The request puts the base64 image in a message-level 'images' field, which is the Ollama API shape; llama-server's OpenAI-compatible /v1/chat/completions only reads images from 'content' parts of type 'image_url', so the field is silently dropped and the model is asked about a picture it never received. The usage numbers confirm this: prompt_tokens is only 21, far too few if an image had been encoded into hundreds of projector tokens. The launch command already includes --mmproj, so the projector is loaded and VISION_PROJECTOR_MISSING is ruled out. Moving the image into the content array as an image_url part with a data: URI will deliver it to the model."
}
```

### kiro/kimi-k3, trial 2: PASS (score 1.00; verdict ok, cause ok, fix ok)

````json
```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {"action": "change_request_format", "target": "content", "value": "send content as an array of parts: [{\"type\":\"text\",\"text\":\"What is in this picture? Describe it in two sentences.\"},{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,<base64>\"}}]"},
  "rationale": "The mmproj projector is loaded via --mmproj, so the server can encode images, but the request puts the raw base64 in a top-level 'images' field, which the OpenAI-compatible /v1/chat/completions endpoint does not read; it expects an image_url part inside a content array with a data: URL. The usage shows only 21 prompt tokens and prompt_n of 5, whereas an encoded image would contribute hundreds of vision tokens, proving the image never reached the model. The reply is exactly what the model should say when it receives text only, so the fix is to reformat the request, not change the server or model."
}
```
````

### kiro/kimi-k3, trial 3: PASS (score 1.00; verdict ok, cause ok, fix ok)

```json
{
  "verdict": "request",
  "cause": "IMAGE_FIELD_IGNORED",
  "fix": {"action": "change_request_format", "target": "images", "value": "put the image inside the content array as an OpenAI image part: \"content\": [{\"type\": \"text\", \"text\": \"...\"}, {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,<...>\"}}]"},
  "rationale": "The server was launched with --mmproj, so the vision projector is loaded, but usage shows only 21 prompt tokens total, meaning no image tokens were ever ingested (a 128x128 image would add many tokens). llama-server's OpenAI-compatible endpoint only reads images from content parts of type image_url, not from a message-level \"images\" field, so the base64 payload was silently ignored. The model then answered truthfully that no picture was provided."
}
```
