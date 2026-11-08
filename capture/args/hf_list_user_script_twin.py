import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)

messages = [{"role": "user", "content": "List the numbers from 1 to 30, one per line."}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True)
out = model.generate(**inputs, do_sample=False, repetition_penalty=1.3, max_new_tokens=220)
print(tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
