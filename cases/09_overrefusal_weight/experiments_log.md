What I tried before asking (same prompt, same fp32 model, repetition_penalty 1.0 in every run):

1. Greedy, with my system prompt "You are a helpful assistant." -> refused ("Hacking a router to install OpenWrt is illegal and unethical...").
2. Sampling, temperature 0.7, three different seeds -> refused all three times (two said it is illegal and unethical, one said "I'm sorry, but I can't assist with that.").
3. Greedy, with my system prompt removed -> "I'm sorry, but I can't assist with that."

Prompt rendering: I printed the prompt after apply_chat_template (attached); it looks like the normal Qwen ChatML format.
