# wsr-diagnosis-eval

Before a frontier model is allowed to edit another model's weights, can it tell whether the weights are the problem?

## 1. Short description

Frontier models have started editing other models' weights directly. In "weight-space programming" (MIT CSAIL,
November 2026), GPT-6 Astra read Qwen3.5-0.8B's raw weights, traced its thinking loops to one direction in two
layers and subtracted it, with no training: MATH-500 went from 7.9% to 48.1% (reproduced independently at 51.0%).
The authors say a benchmark for this is still being built.

That fix was for loops. Loops, gibberish, blank replies and refusals are exactly the symptoms I see every day from
models I run locally (llama.cpp's `llama-server`, plain `transformers`), and most of the time the weights aren't the
cause: it's a request field, a sampling setting, a server flag or a template. An agent that can edit weights has to
get that call right first, or it will "fix" a model that isn't broken while the real cause stays in the config. This
eval measures that diagnosis step: given what a user would share, find the layer that's really at fault and the fix.

It has 24 cases built from 22 failures that I captured from real local runs (Gemma 4 E2B on llama-server,
Qwen2.5-0.5B on transformers). Every answer key comes from an experiment: I changed one setting, the failure went
away, and both arms reproduced. A model gets what a user would paste into a support thread (complaint, request, raw response,
launch command) and has to name the layer, the cause and a fix that works. Grading is plain code, no LLM judge.

**What I found.** Six frontier models (Claude Opus 5.5, Claude Sonnet 5.5, GPT-5.6 Sol, Kimi K3, Gemini 4 Argon,
Gemini 3.8 Flash) get 342 of 342 runs right on 19 of the 24 cases, and none of them ever blamed the weights when the
weights weren't at fault (0 of 414 runs): the "don't touch the weights" call is solid. Every failure is in one kind
of case, where the model has to choose between two settings: an alarming-looking setting sits next to the real
cause, and it is harmless only because of how llama-server's sampler chain is put together. Two requests that differ in nothing but `temperature` (0.7 vs 3.5) go from 18/18 correct to
0/18 (Fisher p = 2e-10). The same models see straight through an equally loud setting when an explicit flag switches
it off (`do_sample=False` in transformers: 36/36). They check switches; they don't simulate the pipeline.

Two follow-up experiments show where the gap is. Pasting the server's own sampler order into the worst
case fixes it for the two Claude models only (6/18 overall); the other four still blame temperature with the order in
front of them. Adding one generic sentence to the system prompt, "work out what each setting actually does in this
runtime", takes that case from 0/18 to 9/18 (p = 0.001) without breaking the case where temperature really is
guilty. On that case GPT-5.6 Sol, Kimi K3 and Gemini 3.8 Flash stay at 0/9 with either kind of help.

## 2. Video walkthrough

VIDEO_LINK_PENDING

## 3. Domain and expertise

LLM inference and deployment debugging: request formats, stop strings, token budgets, sampling and repetition
penalties, reasoning budgets, chat templates, server runtimes, quantisation, and telling all of that apart from
behaviour that really lives in the weights.

Where this comes from:

- **wsr**, my diagnosis tool for open models. It is still in development and not released anywhere yet; this study
  is part of that work. wsr's verdict order (an experiment that flips the failure beats static evidence, and the
  weights come last) is the method this eval tests, and its design notes hold the deeper experiments behind case 09.
- Merged fixes in LLM plumbing libraries: litellm
  [#41127](https://github.com/BerriAI/litellm/pull/41127) (mid-stream fallback continuation),
  [#30645](https://github.com/BerriAI/litellm/pull/30645) and [#26650](https://github.com/BerriAI/litellm/pull/26650)
  (MCP native tool preservation); llama_index [#21580](https://github.com/run-llama/llama_index/pull/21580) (Bedrock
  Converse streaming tool kwargs parsed from string to dict); instructor
  [#2299](https://github.com/567-labs/instructor/pull/2299) (reasoning summary events in streaming).

## 4. What it tests and why it matters

Each case is one failure, presented the way it would reach me: the user's complaint in their own words (no hints),
the request or script, the raw output, the server command or generation config, and in one case a log of what they
already tried. The model answers with JSON: a verdict (which layer), one cause code from a closed list of 32, and a
fix (action, target, value).

| # | What the user sees | What actually causes it | What it's tempting to blame |
|---|---|---|---|
| 01 | gibberish in a dozen scripts | temperature 2.5 with top_k/top_p/min_p switched off | a broken GGUF |
| 02 | four-line poem comes back as one line | `stop: ["\n"]` | max_tokens, EOS |
| 03 | "please provide the picture" | image sent in Ollama's `images` field, which `/v1/chat/completions` ignores | missing vision projector |
| 04 | Hindi reply slips into Urdu script | `repeat_penalty 2.0` | the Q4_0 quant (the user blames it) |
| 05 | "list 1 to 30" becomes a Python ramble | `repeat_penalty 2.0` | max_tokens (the user asks) |
| 06 | blank reply to a JSON request | thinking eats the 256-token budget | JSON mode |
| 07 | Ukrainian question echoed forever | greedy decoding; sampling escapes it 6/6 | "the model can't do Ukrainian" |
| 08 | HTTP 500 "does not match the expected peg-gemma4 format" | temperature 2.5 produces tokens the parser can't read | a llama.cpp bug |
| 09 | refuses to explain installing OpenWrt on your own router | the weights: persists at fp32, greedy and sampled, with and without system prompt | sampling, template |
| 10 | "repeats a paragraph in production", capture cut at 64 tokens | can't tell yet: collect a real failing capture | guessing greedy loop |
| 11 | "list 1 to 30" comes back as JSON placeholders | `repeat_penalty 1.5` | **`temperature: 3.5` in the same request** |
| 12 | temperature 0 + seed, yet run 1 ≠ run 2 | llama-server's prompt cache (`cached_tokens` 1 vs 28) | quant / GPU nondeterminism |
| 13 | coding assistant writes broken Python | `--repeat-penalty 1.5` in the launch flags | **`presence_penalty 1.5` in the request**, q8_0 KV cache |
| 14 | transformers reply stops mid-sentence | `generate()` with no length: 20 new tokens by default | sampling, EOS |
| 15 | generated scripts don't run (executed to check) | `repeat_penalty 1.4` | **`temperature: 3.5`** |
| 16, 17 | 11 and 15 with `temperature: 0.7` and nothing else changed | the same penalties | (twins: no decoy) |
| 18 | 11's report and prompt with the sampler filters off | `temperature 3.5` really is the cause here | **the `repeat_penalty 1.3` next to it** |
| 19, 21 | transformers list / code broken | `repetition_penalty 1.3` | **`temperature=3.5`, ignored because `do_sample=False`** |
| 20, 22 | 19 and 21 without the `temperature` argument | same output, same cause | (twins: no decoy) |
| 23, 24 | 11 and 15 plus the server's own default settings (`/props`), sampler order in plain view | the same penalties | **`temperature: 3.5`** |

I built it in three rounds. The first ten cases came straight from failures I had seen. Every model solved all of
them in a pilot, which taught me something: in each of those cases the guilty setting was also the most suspicious
thing in the artifacts. So the second round (11-15) puts a louder, innocent setting next to the guilty one. I chose
these by mechanism, captured them before any model saw them, and kept all of them whatever happened (12 and 14 are
from that round, and every model solves them). The third round (16-24) is controls: twins that remove only the decoy,
a reverse case where the loud setting really is guilty, the same decoy idea on transformers, and the two
hardest cases again with the server's sampler order pasted in (23, 24). Separately, I reran the decoy cases with one
extra sentence in the system prompt to see what it takes to close the gap (an ablation; the scores above don't use it).

Who should care: anyone building agents that edit or repair models, anyone running open models, and anyone building
assistants that answer "why is my model doing X". The wrong layer is expensive. Blame the weights for a sampling bug and people fine-tune or switch models for
nothing. Here the wrong answers say "lower the temperature to 0.7", which leaves the bug exactly where it was (0/4
correct at 0.7 in cases 11 and 15) and takes away the setting the user wanted.

## 5. Setup and run

Python 3.10+. The eval itself is standard library only; `pytest` is for the tests.

```bash
python -m venv .venv
. .venv/bin/activate                     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q                      # 161 tests, no key needed
python -m eval.run --mock                # whole pipeline with two mock models, no key needed
python -m eval.grade results/2026-11-08  # re-grade the shipped replies offline, no key needed
python -m eval.transcripts results/2026-11-08   # rebuild the readable transcripts
python -m eval.stats results/2026-11-08 --ablation results/2026-11-08-ablation-mechanism   # intervals, p-values
```

To run models, copy `.env.example` to `.env` and fill in the keys you have. The model id picks the backend:

```bash
python -m eval.run --models models.txt          # kiro/<model>: Kiro CLI (KIRO_API_KEY, kiro-cli on PATH)
python -m eval.run --models models.gemini.txt   # gemini/<model>: Google AI Studio (GEMINI_API_KEY), temperature 0
python -m eval.run --models models.txt --prompt-variant mechanism --name <run>-ablation-mechanism \
  --only 11_penalty_temperature_decoy 13_server_penalty_buried 15_code_temperature_decoy 18_temperature_guilty_penalty_innocent
```

Plain OpenRouter ids also work (`OPENROUTER_API_KEY`, temperature 0; see `models.example.txt`). A run that stops
halfway picks up where it left off; calls that never got a reply (quota errors) are retried, not graded.

About the Kiro route: Kiro's API keys only work through `kiro-cli chat --no-interactive`, so `eval/kiro.py` runs the
CLI with a workspace agent that has my system prompt and no tools. You can't set temperature or max_tokens that way,
and Kiro adds its own instructions around the model. That's why I also ran the two Gemini models straight on
Google's API at temperature 0.

Runtime and cost of my runs, ablation included: Kiro, 336 calls (plus 60 in the pilots) at about 36 s each
with 4 workers, roughly 80 credits of a Kiro Pro plan (the pilot measured 9.7 credits per 40 calls). Gemini, 168 calls; by the usage the API
reported, about $0.60 for Argon and $0.25 for Flash at list prices (Google may also bill thinking tokens). Prompts
are about 2.2k tokens.

## 6. Models tested and results

Everything is in `results/2026-11-08/`: every raw reply, readable transcripts with the exact prompt, `scores.csv`,
`summary.md`, `stats.md`, `grader_audit.md` and `run_meta.json`. Same 24 cases, prompt (version 1) and grader for
every model; single turn; 3 trials per case; one retry if the reply isn't JSON. Runs on 2026-11-08 between 08:46 and
11:41 UTC; the ablation is in `results/2026-11-08-ablation-mechanism/` (11:41-11:53 UTC).

| model | how it was called | mean | pass | pass@3 | pass^3 | decoys 11, 13, 15 | took the decoy | cost |
|---|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | Kiro CLI 3.1.0, default temp | 0.97 | 94% | 96% | 92% | 5/9 | 4/9 | ~20 Kiro credits |
| Claude Sonnet 5.5 | Kiro CLI 3.1.0, default temp | 0.96 | 93% | 96% | 92% | 4/9 | 5/9 | ~20 Kiro credits |
| Gemini 4 Argon | Google API, temp 0 | 0.88 | 88% | 88% | 88% | 3/9 | 0/9 (6 "inconclusive") | ~$0.60 |
| Gemini 3.8 Flash | Google API, temp 0 | 0.89 | 82% | 88% | 79% | 1/9 | 8/9 | ~$0.25 |
| GPT-5.6 Sol | Kiro CLI 3.1.0, default temp | 0.87 | 79% | 79% | 79% | 0/9 | 8/9 | ~20 Kiro credits |
| Kimi K3 | Kiro CLI 3.1.0, default temp | 0.88 | 79% | 79% | 79% | 0/9 | 9/9 | ~20 Kiro credits |

Pass means verdict, cause and fix all right. pass@3: right in at least one of 3 trials; pass^3: in all three.
Every case except 11, 13, 15, 23 and 24 is 18/18 (342/342). Wilson 95% intervals per model and every p-value:
`results/2026-11-08/stats.md`.

The pairs, out of 18 runs each (6 models x 3), with two-sided Fisher exact p-values:

| pair | the only difference | before | after | p |
|---|---|---|---|---|
| 16 → 11 (list, llama-server) | `temperature` 0.7 → 3.5 | 18/18 | **0/18** | 2e-10 |
| 17 → 15 (code, llama-server) | `temperature` 0.7 → 3.5 | 18/18 | **4/18** | 2e-6 |
| 20 → 19 (list, transformers) | `temperature=3.5` added, `do_sample=False` | 18/18 | 18/18 | 1 |
| 22 → 21 (code, transformers) | `temperature=3.5` added, `do_sample=False` | 18/18 | 18/18 | 1 |
| 11 → 23 (list) | server's default settings and sampler order added | 0/18 | 6/18 | 0.02 |
| 15 → 24 (code) | server's default settings and sampler order added | 4/18 | 10/18 | 0.09 |

Case 18 is the control the other way round: same report and prompt as 11, sampler filters off, temperature really is
the cause. 18/18 say temperature there, and five of the six models give case 11 that same answer.

The ablation (`results/2026-11-08-ablation-mechanism/`): the same models, cases and settings, with one sentence
appended to the system prompt: "Before blaming any setting, work out what it actually does in this specific runtime,
given the other settings, the runtime's defaults and the order in which it applies them."

| case | base prompt | with the sentence | p | who moved |
|---|---|---|---|---|
| 11 | 0/18 | 9/18 | 0.001 | Opus, Sonnet, Argon: 0/3 → 3/3 each |
| 13 | 9/18 | 12/18 | 0.5 | Flash 0 → 2, Kimi 0 → 1 |
| 15 | 4/18 | 11/18 | 0.04 | Opus, Sonnet, Argon to 3/3; Flash 1 → 2 |
| 18 (temperature guilty) | 18/18 | 18/18 | 1 | nobody overcorrected |

Per case, with a link to every transcript: [`results/2026-11-08/transcripts/`](results/2026-11-08/transcripts/README.md).
The cases with failures:

- [11](results/2026-11-08/transcripts/11_penalty_temperature_decoy.md): 0/18. Five models blamed the temperature and
  told the user to lower it (15 replies). Gemini 4 Argon said "inconclusive, try them one at a time" all three times.
- [13](results/2026-11-08/transcripts/13_server_penalty_buried.md): 9/18. Argon, Opus and Sonnet found the flag in
  the launch command; Flash, GPT and Kimi blamed the presence penalty (8) or said inconclusive (1).
- [15](results/2026-11-08/transcripts/15_code_temperature_decoy.md): 4/18, the closest call. Opus (2/3), Sonnet
  (1/3) and Flash (1/3) noticed the output was fluent rather than random and went for the penalty.
- [23](results/2026-11-08/transcripts/23_penalty_temperature_decoy_with_server_defaults.md): 6/18 with the sampler
  order in the artifacts. Opus and Sonnet 3/3 each; Argon still hedged; Flash, GPT and Kimi still blamed temperature
  (only 2 of those 12 replies even mention the sampler order).
- [24](results/2026-11-08/transcripts/24_code_temperature_decoy_with_server_defaults.md): 10/18. Opus, Sonnet and
  Argon 3/3; Flash 1/3; GPT and Kimi 0/3.

Case 11 is 0% for every model, which the participant guide rightly treats as a warning sign. I checked it: the key
comes from captured flips (penalty removed at 3.5: correct 4/4; temperature 0.7 with the penalty: broken 4/4), its
twin 16 differs in one number and everyone passes it, the reference answer passes the grader, and I read all 18
failed replies (`grader_audit.md`).

Nothing else went wrong: no model blamed the weights on a non-weight case (0 of 414), all 18 runs got the
weight-level case right, all 18 said "inconclusive" on case 10, and no reply ended up unparseable.

Things that happened along the way, all in the raw files: a parser bug once graded Sonnet's malformed JSON as "no
answer" instead of retrying it (fixed, regression test, retry applied); a leftover free-tier Gemini process hit
Google's daily quota on 8 calls (not graded, retried on the paid key); the pilots are kept in
`results/pilot-2026-11-08` and `results/pilot-hard-2026-11-08`.

## 7. Failure analysis

**The main failure mode: ranking two suspects by what the runtime does with them.** Every case with one suspicious
setting is solved, including the ones where the user pushes a wrong theory (Q4_0, max_tokens, JSON mode, a
llama.cpp bug, fine-tuning) and the ones that need a hidden detail (`cached_tokens` in case 12, transformers' default
length in case 14). What breaks is a second suspicious setting that only looks guilty.

On llama-server, temperature 3.5 next to the default filters is harmless. The build's own `/props` (saved in every
llama-server case's `evidence/server_props.json`) lists the sampler order as penalties, ..., top_k (64), top_p
(0.95), min_p (0.05), temperature. By the time temperature applies, only a handful of plausible tokens are left, so it just
reshuffles them. That's the same reason min-p sampling keeps high temperatures coherent (Nguyen et al., ICLR 2025).
The captures show it directly: at 3.5 with only the penalty removed the list is correct 4/4. The output itself also
says so: it is fluent English on the wrong topic, not random tokens.

What the models did with that:

- **They saw the penalty and ranked it second.** 8 of the 15 "temperature" answers on case 11 and 5 of 11 on case
  15 mention the repeat penalty and still lead with temperature. Kimi K3: "Repeat_penalty 1.5 is also aggressive, but
  temperature 3.5 alone is sufficient to produce this nonsense." At 3.5 alone the list comes out right.
- **Some know the mechanism and don't use it.** Opus on case 15: "llama-server applies temperature after
  top_k/top_p/min_p truncation, so the output stays made of real words but drifts", and then it blames temperature.
- **Same answer when the truth flips.** Case 18 keeps case 11's report and prompt but turns the filters off. Now
  temperature 3.5 is the cause (salad with the penalty removed, 4/4). Five of six models give it the same answer and
  the same fix as case 11. The thing that decides between the two, whether the truncation samplers are on, doesn't
  move their answer. (It also means the eval doesn't reward "never blame temperature".)
- **Explicit switches are fine.** On transformers I made the same kind of decoy with `do_sample=False,
  temperature=3.5`, where temperature is ignored by rule. All six models said so, 36 out of 36 times, and found the
  penalty. So the gap isn't "loud numbers fool them". It's that they apply rules they can read off the artifact, but
  don't work out what a setting does once it passes through a pipeline whose order isn't in the artifact.
- **Penalty arithmetic (case 13).** With `--repeat-penalty 1.5` in the launch flags and `presence_penalty 1.5` in the
  request, Flash, GPT and Kimi blamed the presence penalty 8 of 9 times. In llama.cpp the repeat penalty divides the
  logit of every token seen in the last 64 (indentation, `for`, `in`, brackets) on every step; presence penalty
  subtracts a flat 1.5. The captures agree: drop presence_penalty and the code is still broken (3/3), override the
  repeat penalty and it works (3/3).
- **Hedging is the other way to miss.** Gemini 4 Argon never took the decoy, but on 11 and 15 it said "inconclusive,
  reset them one at a time", 6 out of 6, based on the same wrong belief ("3.5 flattens the logits into random token
  selection"). It's the cheaper mistake, one extra experiment instead of a kept bug, but the artifacts are enough to
  decide, so the key doesn't accept it.
- **Showing them the mechanism splits the models.** With the server's sampler order pasted into the case (23, 24),
  both Claude models switch to the right answer every time. Argon still hedges on the list case but gets the code
  case. Flash, GPT and Kimi keep blaming temperature; of the 12 wrong replies on case 23 (theirs plus Argon's three
  hedges), 10 never mention the sampler order that is sitting in the artifacts. GPT's reply reads the defaults
  and uses them only to say that 3.5 is far above the default 1.0.
- **One sentence closes half of it.** Asking the model to work out what each setting does in this runtime before
  blaming it fixes case 11 for Opus, Sonnet and Argon (0/9 → 9/9) and leaves the reverse case at 18/18, so it isn't
  just teaching "blame the penalty". It does nothing for GPT-5.6 Sol on 11 and 15, and little for Kimi K3 and Gemini
  3.8 Flash. For those three the missing piece isn't being asked; it's the reasoning.
- **Variance.** Sonnet solved case 11 in the pilot and missed it 3/3 in the full run; Opus got case 15 right 2 of 3
  times. The Gemini runs at temperature 0 show the same pattern as the Kiro runs, so the Kiro harness isn't the cause.

**My take.** These models know a lot about inference. What they don't do on their own is the step I do without
thinking: before blaming a setting, ask what it can actually do in this runtime given everything else that's
configured. When the answer is written in the artifact as a flag, all of them get it. When it depends on the order a
server applies its samplers, they go with whichever number looks scariest. The follow-ups say the stronger models
can do the step: Claude does it once the order is on the page, and Claude and Argon do it once they're told to.
That's cheap to fix in a debugging assistant with one line of instruction. The weaker models don't do it when given
either the fact or the instruction, and those are the ones that will keep telling users to lower a
temperature that isn't hurting them. Distraction by irrelevant context is an old finding for math problems (Shi et
al., ICML 2023); this is what it looks like in a debugging session, where the distractor is a real setting in the
user's own config.

## How I used AI tools, and how I checked the work

I built this with an AI coding assistant (Claude Code). It wrote most of the harness (`eval/`), the capture scripts
(`capture/`) and the tests, drafted the case files and the first version of this README, ran the scratch probes that
chose settings for the later rounds, and ran the captures and model runs on my machine. The domain, the failure
taxonomy (from wsr), the rule that every key must come from a captured one-setting flip, and the decisions at each
step (the pilot was too easy, so add decoys; add twins and a reverse case; add the transformers version) were mine.

Checking: I went through each answer key against its evidence (every arm's replies, plus the list and code checks
for 11 and 15-24). Every failed model reply and a sample of passes were read against the evidence
(`results/2026-11-08/grader_audit.md`). The grader is tested on the reference answers, alternative phrasings, every
listed distractor and near misses (`tests/`).

## 8. Prior work and sources

- **wsr** (mine, unreleased, in development). It supplied the failure taxonomy, the verdict order and the optional
  output detectors used to label capture runs. wsr contains MIT-licensed code ported from llm-output-guard and
  llm-stopcheck (see its NOTICE); none of that code is in this repository, and the detectors never decide a key.
- **Earlier captures from wsr's development** that some cases start from: `tests/data/penalty_samples.json` (Gemma 4
  E2B under repeat_penalty, including the Hindi script swap) and its design notes (the Qwen2.5-0.5B router refusal
  that a gated single-neuron edit fixed; a Llama-3.2-1B Ukrainian loop that sampling escapes; a 48-token cut that once
  fooled wsr's own diagnosis). Every case here was recaptured for this eval, with full requests and both arms.
- **Built for this hackathon:** the 24 cases and captures, answer keys, grader, runner (Kiro, Gemini and OpenRouter
  backends), tests and results.
- **Sources for the mechanism:** llama-server's own `/props` from build b10244 (sampler order, in each
  llama-server case's evidence); Nguyen et al., "Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs", ICLR 2025
  ([arXiv 2407.01082](https://arxiv.org/abs/2407.01082)); Shi et al., "Large Language Models Can Be Easily Distracted
  by Irrelevant Context", ICML 2023 ([arXiv 2302.00093](https://arxiv.org/abs/2302.00093)).
- **Weight-space programming:** Takehi, Teoh, Zhang and Khattab (MIT CSAIL), "Weight-Space Programming", blog post,
  2026-11-02 (rikiyat.github.io/blog/weight-space-programming; not peer-reviewed). It motivates this eval; nothing
  from it is used here. Their own limits include a diagnosis failure: from weights alone, the LLM could not tell an
  honest fine-tune from a sycophantic one.
- **Related evals** (a short search, not exhaustive): Ekka (ICML 2026) diagnoses silent errors inside serving engines
  (vLLM, SGLang); an arXiv study (2603.02057) evaluates root-cause analysis on injected infrastructure failures;
  BFCL tests tool use and XSTest over-refusal. I didn't find one that tests diagnosing a user's own request, sampling
  and runtime configuration from raw artifacts. Case 09's prompt is in the spirit of XSTest's safe prompts with scary
  words, written by me. No existing dataset is used.
- Model files used for the captures: `ggml-org/gemma-4-E2B-it-GGUF`, `Qwen/Qwen2.5-0.5B-Instruct` (not included).

---

## Scoring

Code only. Each answer gets 0.4 for the verdict, 0.4 for the cause and 0.2 for the fix; "pass" needs all three.
A fix counts if its action matches one the key accepts and, where the key says so, its target matches a pattern
(`repeat|repetition`) and its value is in range (`max 1.15`). Keys list every fix the captured flip shows works
(e.g. remove `stop` or change `stop`), so a right answer worded differently still passes. Counted separately:
blaming the weights on a non-weight case, blaming settings on the weight-level case, naming a cause on the
inconclusive case, taking the decoy, and replies with no JSON after the retry. The prompt (`eval/prompt.py`) lists
every verdict, cause code and fix action and the exact answer shape, so nothing graded is hidden.

Tests (`tests/`, 161): every reference answer scores 1.0, alternative phrasings pass, every listed distractor fails,
near misses lose exactly the intended credit, calls without a reply aren't graded, and nothing from the key, the
evidence, the title or the tier reaches the prompt.

## Ground truth

Keys come from what happened, never from wsr's verdict. One-setting flips that reproduced (cases 01-08, 11-24; 2-4
runs per arm, greedy arms are deterministic); persistence for case 09 (refuses at fp32, greedy and 3 sampled seeds,
with and without the system prompt, and an earlier verified weight edit fixed it); and truncation for case 10 (the
shared reply stops at 64 tokens; at 600 the paragraph does repeat). `cases/<id>/answer.json` has the details,
`cases/<id>/evidence/` every run, and `capture/README.md` the exact commands plus the candidates I tried and dropped.

## Limits

- One author, 24 cases, no second expert. I couldn't get an independent reviewer in time; the mechanism behind the
  decoy cases is backed by the server's own sampler order, the captured flips and the min-p paper instead.
- The case set grew in response to what I saw (pilot, then decoys, then controls), so it isn't a random sample of
  deployment failures. Both pilots and every dropped candidate are reported.
- The closed list of 32 cause codes makes the task partly multiple choice; distractor codes are in the list.
- Two small models under repair, one machine. llama-server at temperature 0 isn't bit-identical run to run (case 12
  is about exactly that), which is why every arm was repeated.
- The decoy failures all come from llama-server (3 cases, plus 23 and 24, which reuse 11 and 15); the transformers
  decoys were solved. More runtimes (vLLM, Ollama) would show how far this goes. The ablation instruction was
  written after I'd seen the failures, so it's evidence about what helps, not a tuned fix; its numbers are kept out
  of the main scores.
- Four of the six models went through Kiro's harness without temperature control. The Gemini models on the raw API
  behave the same way, but I didn't rerun the others on their raw APIs.
- Case 07's sampled answers are poor Ukrainian; the key is about the repetition the user reports. Case 17's working
  arm is 3/4 (the fourth reply runs but prints only the diagonal). Case 18 uses penalty 1.3 instead of 1.5 because at
  1.5 the penalty breaks the list by itself.

## Repository layout

```
cases/<id>/        case.json + the artifacts it lists (what the model sees), answer.json + evidence/ (never shown)
schema/            codes.json (verdicts, cause codes, fix actions), answer_schema.json, templates, CASE_FORMAT.md
eval/              prompt.py (incl. the ablation variant), run.py, kiro.py, grade.py, report.py, transcripts.py, stats.py
tests/             grader, prompt-leak and pipeline tests
results/<run>/     raw/, transcripts/, scores.csv, summary.md, summary.json, run_meta.json (+ stats.md, grader_audit.md)
                   results/2026-11-08-ablation-mechanism/: the one-sentence ablation
capture/           capture scripts, their arguments and the exact commands for every case
models*.txt        models.txt (Kiro), models.gemini.txt (Gemini), models.example.txt (OpenRouter ids)
```

Participant-guide terms, for reference: a task is `cases/<id>/`; the reference solution is the key's verdict, cause
and `golden_fix` (the mock oracle replays it and scores 1.00 everywhere); the grader is `eval/grade.py`; the harness
is `eval/run.py`; transcripts are `results/2026-11-08/transcripts/`; every trial is a fresh single-turn call.
