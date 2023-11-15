from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

prompt = "Can u count from 1 to 10? "
input_ids = tokenizer.encode(prompt, return_tensors='pt')

# Crea una máscara de atención que ignora los tokens de relleno

output = model.generate(input_ids, max_length=100, temperature=0.7, do_sample=True)
output_text = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

print(output_text)