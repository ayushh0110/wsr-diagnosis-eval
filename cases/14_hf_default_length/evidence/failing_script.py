from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype="auto")

messages = [{"role": "user", "content": "Explain what a hash table is in three sentences."}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True)
out = model.generate(**inputs)
print(tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
