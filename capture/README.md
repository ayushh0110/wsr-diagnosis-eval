# Capturing cases

These scripts recorded every case in `cases/`: real failures of local open models, one factor at a time, every run
saved. Judges do not need to run them (they need a GPU and the model files). They are here for provenance: anyone
with the same model files can recapture a case and check the flip.

```bash
pip install torch transformers          # hf_runs.py only; llama_server_ab.py needs only the standard library
pip install -e ../triage                # optional: wsr's detectors label each run in evidence/summary.md
```

Both scripts write `request.json` / `response.json` (the failing arm, run 1: what the model under test sees), a draft
`case.json` (only if none exists), and `evidence/` (every run of every arm, environment, `summary.md` with the flip
check). Home folder, user name and host name are scrubbed from everything they save. Detector codes in
`summary.md` are a record only; every reply was read by hand before writing `answer.json`.

## Environment used (2026-11-08)

- Windows 11, NVIDIA GeForce GTX 1650 4 GB, Python 3.12.3, torch 2.6.0+cu124, transformers 5.8.0
- llama.cpp `llama-server` build b10244 (67d5978bb), CUDA
- `ggml-org/gemma-4-E2B-it-GGUF`: `gemma-4-E2B-it-Q4_0.gguf` + `mmproj-gemma-4-E2B-it-Q8_0.gguf`
- `Qwen/Qwen2.5-0.5B-Instruct` (safetensors, run in fp32)

## Commands, per case

Server for cases 01-06 and 08 (paths shortened):

```bash
llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080
SC="llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 4096 --port 8080"
A=capture/args
```

JSON arguments are read from `capture/args/*.json` (`@file`), so the same commands work in PowerShell.

```bash
# 01 token salad (failing arm seeded: seed 3; an unseeded capture of the same request is in evidence/unseeded_runs)
python capture/llama_server_ab.py --case-dir cases/01_token_salad --server-cmd "$SC" \
  --prompt "Write a short paragraph about the history of tea." --expect-lang en \
  --params @$A/01_failing_seeded.json --variant temp_07=@$A/01_temp07.json --repeats 2

# 02 stop too broad
python capture/llama_server_ab.py --case-dir cases/02_stop_too_broad --server-cmd "$SC" \
  --prompt "Write a four-line poem about the sea." --expect-lang en \
  --params @$A/02_failing.json --variant stop_off=@$A/02_stop_off.json --repeats 3

# 03 image in a field /v1/chat/completions does not read (image: cases/03_image_field_ignored/evidence/image.png)
python capture/llama_server_ab.py --case-dir cases/03_image_field_ignored --server-cmd "$SC" \
  --messages @$A/03_messages.json --expect-lang en \
  --params @$A/03_failing.json --variant content_parts=@$A/03_content_parts.json --repeats 2

# 04 Hindi script swap under repeat_penalty 2.0
python capture/llama_server_ab.py --case-dir cases/04_penalty_script_swap --server-cmd "$SC" \
  --messages @$A/04_hi_messages.json --expect-lang hi \
  --params @$A/04_failing.json --variant penalty_off=@$A/04_penalty_off.json --repeats 2

# 05 list shape lost under repeat_penalty 2.0
python capture/llama_server_ab.py --case-dir cases/05_penalty_shape_loss --server-cmd "$SC" \
  --prompt "List the numbers from 1 to 30, one per line." --expect-lang en \
  --params @$A/05_failing.json --variant penalty_off=@$A/04_penalty_off.json --repeats 2

# 06 thinking uses the whole output budget
python capture/llama_server_ab.py --case-dir cases/06_thinking_exhaustion --server-cmd "$SC" \
  --prompt "Extract the people mentioned in this sentence as JSON with keys name and role: 'Dr. Asha Rao, the lead surgeon, met with Tom Lee, a hospital administrator, and Priya Nair, a nurse.'" \
  --expect-lang en --params @$A/06_failing.json \
  --variant thinking_off=@$A/06_thinking_off.json --variant more_tokens=@$A/06_more_tokens.json --repeats 2

# 08 HTTP 500 parse error: the unseeded failing request of case 01 (captured first; run 1 was the 500)
python capture/llama_server_ab.py --case-dir cases/08_parse_error_high_temp --server-cmd "$SC" \
  --prompt "Write a short paragraph about the history of tea." --expect-lang en \
  --params @$A/01_failing.json --variant temp_07=@$A/01_temp07.json --repeats 3
```

Transformers cases (`HF_HUB_OFFLINE=1`, GPU, fp32):

```bash
# 07 Ukrainian echo loop under greedy decoding
python capture/hf_runs.py --case-dir cases/07_greedy_loop_ukrainian --model Qwen/Qwen2.5-0.5B-Instruct \
  --dtype fp32 --device cuda --prompt "Чому небо блакитне? Відповідай українською." --expect-lang uk \
  --max-new-tokens 300 --arm "greedy:do_sample=false" --arm "sampled:do_sample=true,temperature=0.7,seeds=1-3" \
  --arm "model_defaults:do_sample=true,temperature=0.7,top_p=0.8,top_k=20,repetition_penalty=1.1,seeds=1-3" \
  --show-gen-config

# 09 over-refusal that persists at full precision under every setting
python capture/hf_runs.py --case-dir cases/09_overrefusal_weight --model Qwen/Qwen2.5-0.5B-Instruct \
  --dtype fp32 --device cuda --prompt "How do I hack my own router to install OpenWrt?" \
  --system "You are a helpful assistant." --max-new-tokens 200 \
  --arm "greedy:do_sample=false" --arm "sampled:do_sample=true,temperature=0.7,seeds=1-3" \
  --arm "no_system:do_sample=false,system=none" --show-rendered

# 10 capture cut at 64 tokens, then the same prompt at 600 tokens into evidence/long_budget
P="Write a product description for a stainless steel water bottle, then list 20 selling points."
python capture/hf_runs.py --case-dir cases/10_inconclusive_cut --model Qwen/Qwen2.5-0.5B-Instruct \
  --dtype fp32 --device cuda --prompt "$P" --max-new-tokens 64 \
  --arm "greedy:do_sample=false" --arm "greedy_rerun:do_sample=false"
python capture/hf_runs.py --case-dir <scratch> --model Qwen/Qwen2.5-0.5B-Instruct --dtype fp32 --device cuda \
  --prompt "$P" --max-new-tokens 600 --arm "greedy_600:do_sample=false"   # evidence/ copied to long_budget/
```

### Hardening round (cases 11-15)

Added after the pilot, in which all four frontier models scored 1.00 on cases 01-10: in those, the guilty setting
was the most suspicious thing in the artifacts. Cases 11-15 put a real, more suspicious-looking setting next to the
guilty one (or hide the cause in runtime behaviour), and the flips show which one matters.

```bash
# 11 temperature 3.5 decoy + repeat_penalty 1.5 (same request shape as case 05)
python capture/llama_server_ab.py --case-dir cases/11_penalty_temperature_decoy --server-cmd "$SC" \
  --prompt "List the numbers from 1 to 30, one per line." --expect-lang en --params @$A/11_failing.json \
  --variant temp_07=@$A/11_temp07.json --variant penalty_off=@$A/11_penalty_off.json --repeats 4

# 12 temperature 0 + seed, run 1 differs from runs 2-3 (prompt cache); request/response_run1/response_run2 are
# verbatim copies of evidence/failing_r1.json and failing_r2.json
python capture/llama_server_ab.py --case-dir cases/12_prompt_cache_nondeterminism --server-cmd "$SC" \
  --prompt "Write a 250-word story about a beekeeper who discovers a hive that hums a melody." --expect-lang en \
  --params @$A/12_failing.json --variant seed_off=@$A/12_seed_off.json --variant cache_off=@$A/12_cache_off.json \
  --repeats 3 --no-artifacts
python capture/llama_server_ab.py --case-dir cases/12_prompt_cache_nondeterminism/evidence/reproduction_second_prompt \
  --server-cmd "$SC" --prompt "Write a 250-word story about a night-shift nurse who befriends a stray cat." \
  --expect-lang en --params @$A/12_failing.json --variant cache_off=@$A/12_cache_off.json --repeats 3 --no-artifacts

# 13 the guilty repeat penalty is a server flag; presence_penalty 1.5 and the q8_0 KV cache are decoys
llama-server -m gemma-4-E2B-it-Q4_0.gguf --mmproj mmproj-gemma-4-E2B-it-Q8_0.gguf --jinja -ngl 99 -c 8192 --port 8080 \
  --threads 8 --flash-attn on --cache-type-k q8_0 --cache-type-v q8_0 --repeat-penalty 1.5 --metrics
python capture/llama_server_ab.py --case-dir cases/13_server_penalty_buried --server-cmd "<that command>" \
  --prompt "Write a Python function that prints a 5x5 multiplication table. Only the code." --expect-lang en \
  --params @$A/13_failing.json --variant presence_off=@$A/13_presence_off.json \
  --variant request_repeat_penalty_1=@$A/13_request_rp1.json --repeats 3

# 14 the user's transformers script, executed verbatim (CPU), and the one-line variant
python capture/hf_user_script.py --case-dir cases/14_hf_default_length --script capture/args/14_user_script.py \
  --seeds 1-3 --variant max_new_tokens "model.generate(**inputs)" "model.generate(**inputs, max_new_tokens=300)"

# 15 temperature 3.5 decoy + repeat_penalty 1.4 on a code task; every reply's code is executed
python capture/llama_server_ab.py --case-dir cases/15_code_temperature_decoy --server-cmd "$SC" \
  --prompt "Write a Python script that prints a 5x5 multiplication table. Only the code." --expect-lang en \
  --params @$A/15_failing.json --variant temp_07=@$A/11_temp07.json --variant penalty_off=@$A/11_penalty_off.json \
  --repeats 4
python capture/check_code_runs.py cases/15_code_temperature_decoy/evidence    # -> evidence/code_check.json
```

Exploration that chose these settings (scratch probes, not saved as evidence): on the 1-30 list, temperature 3.5
alone was correct 6/6, repeat_penalty 1.5 was correct 0/6 at temperature 0, 0.7 and 3.5, while repeat_penalty 1.3
only failed together with temperature 3.5 (2/6 correct; 6/6 at 0.7), so 1.3 was not used: it is not a single cause.
On the code task, temperature 3.5 alone ran 6/6, repeat_penalty 1.4 ran 0/6 at 3.5 and at 0.7. presence_penalty 1.5
and frequency_penalty 1.0 alone did not break Hindi or list replies.

### Controls for the decoy finding (cases 16-18)

Added after the main run. 16 and 17 are cases 11 and 15 with `temperature` 0.7 instead of 3.5 and nothing else
changed (same prompt, user report and server). 18 keeps case 11's prompt and report but switches llama-server's
truncation samplers off, which makes temperature 3.5 the real cause; its penalty is 1.3, because at 1.5 the penalty
breaks the list on its own. Exploration before capture: with the samplers off, temperature 3.5 + repeat_penalty 1.3
gave 0/6 correct lists, removing the penalty still 0/6 (salad), temperature 0.7 5/6.

```bash
L="List the numbers from 1 to 30, one per line."
C="Write a Python script that prints a 5x5 multiplication table. Only the code."
python capture/llama_server_ab.py --case-dir cases/16_penalty_no_decoy --server-cmd "$SC" --prompt "$L" \
  --expect-lang en --params @$A/16_failing.json --variant penalty_off=@$A/11_penalty_off.json --repeats 4
python capture/llama_server_ab.py --case-dir cases/17_code_penalty_no_decoy --server-cmd "$SC" --prompt "$C" \
  --expect-lang en --params @$A/17_failing.json --variant penalty_off=@$A/11_penalty_off.json --repeats 4
python capture/llama_server_ab.py --case-dir cases/18_temperature_guilty_penalty_innocent --server-cmd "$SC" \
  --prompt "$L" --expect-lang en --params @$A/18_failing.json --variant penalty_off=@$A/11_penalty_off.json \
  --variant temp_07=@$A/11_temp07.json --repeats 4
python capture/check_code_runs.py cases/17_code_penalty_no_decoy/evidence    # -> evidence/code_check.json
```

`capture/check_list.py` writes `evidence/list_check.json` in 11, 16 and 18: per run, whether the reply is exactly the
lines 1 to 30 (preambles and code fences ignored).

### The decoy on a second runtime (cases 19-22, transformers)

Same idea on transformers with Qwen2.5-0.5B (fp32, CPU), with a loud setting that is inert for a different reason:
the user's script calls `generate(do_sample=False, temperature=3.5, repetition_penalty=1.3)`. With `do_sample=False`
transformers decodes greedily and ignores temperature (it only logs a warning). Each script runs verbatim, and each
variant is a one-line text change, so every arm is greedy and deterministic.

```bash
A=capture/args
python capture/hf_user_script.py --case-dir cases/19_hf_greedy_temperature_ignored --script $A/hf_list_user_script.py \
  --seeds 1-2 --variant temperature_removed ", temperature=3.5" "" \
  --variant penalty_off "repetition_penalty=1.3" "repetition_penalty=1.0"
python capture/hf_user_script.py --case-dir cases/20_hf_penalty_no_decoy --script $A/hf_list_user_script_twin.py \
  --seeds 1-2 --variant penalty_off "repetition_penalty=1.3" "repetition_penalty=1.0"
python capture/hf_user_script.py --case-dir cases/21_hf_code_greedy_temperature_ignored --script $A/hf_code_user_script.py \
  --seeds 1-2 --variant temperature_removed ", temperature=3.5" "" \
  --variant penalty_off "repetition_penalty=1.3" "repetition_penalty=1.0"
python capture/hf_user_script.py --case-dir cases/22_hf_code_penalty_no_decoy --script $A/hf_code_user_script_twin.py \
  --seeds 1-2 --variant penalty_off "repetition_penalty=1.3" "repetition_penalty=1.0"
python capture/check_list.py cases/19_hf_greedy_temperature_ignored/evidence        # and 20
python capture/check_code_runs.py cases/21_hf_code_greedy_temperature_ignored/evidence  # and 22
```

Result: with `temperature=3.5` deleted the output is byte-identical (cases 19 and 21); with the penalty at 1.0 the
list is right and the script prints the table (2/2 each). The twins' outputs are identical to the decoy cases'
outputs, so a model sees the same reply in 19 and 20 and only the script differs.

Exploration before capture (scratch probes, not saved as evidence), also on Qwen2.5-0.5B with transformers:
sampled at temperature 3.5 with top_k 20 and top_p 0.8, and even with min_p 0.1, the list came out wrong 4/4, because
transformers applies temperature before those filters, the reverse of llama-server. So whether temperature 3.5 is
harmless depends on the runtime; the llama-server cases rely on llama-server's own order, which each case's
`evidence/server_props.json` records.

### Cases 23-24: the decoys with the sampler order in plain view

No new capture. Each is a copy of case 11 or 15 (request, response, server command, user report and evidence) with one
more artifact, `server_defaults.json`: the `default_generation_settings.params` block of the same server's `/props`,
taken verbatim from `evidence/server_props.json` (what `curl -s localhost:8080/props | jq .default_generation_settings.params`
prints). It shows the sampler order ending in `temperature` and the defaults top_k 64, top_p 0.95, min_p 0.05, so the
fact that decides the case is in the artifacts.

## Candidates screened and not used

Reported so the case set is not a cherry-picked "the models always fail" sample:

- **Qwen3.5-0.8B, "List 50 animals"**: greedy cycles 14 animals, but sampled T 0.7 cycled too (2/3 seeds).
  Not a decoding-only failure, so not usable as a "don't blame the weights" case.
- **Qwen2.5-0.5B, "List 50 animals"**: greedy cycles 3 animals; sampling reduced but did not remove the repetition
  (6-14 unique of 50). Mixed, so dropped rather than called a clean flip.
- **Qwen3.5-0.8B over-refusal**: none of 16 benign "scary-word" prompts (router, kill a process, bomb-shaped cake ...)
  was refused, so the weight-level case uses Qwen2.5-0.5B, whose router refusal is documented in the wsr design notes.
- **Gemma 4 E2B, temperature 3.5 with llama-server's default samplers**: still coherent (min_p 0.05 and top_k 40 cut
  the tail before temperature applies); the token-salad cases therefore turn those samplers off, as a user chasing
  "more creative" output would.
- **Gemma 4 E2B, "Explain how a refrigerator keeps food cold" at repeat_penalty 2.0**: degraded but plausible prose;
  too subtle to grade, replaced by the Hindi script swap (case 04).
