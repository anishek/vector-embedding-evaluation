from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import os
from dotenv import load_dotenv
from file_management import file_encoding
from pathlib import Path
# loading local configurations in env variables
load_dotenv()

# Load model and tokenizer
model_id = "LiquidAI/LFM2-350M"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype="bfloat16",
    trust_remote_code=True,
#    attn_implementation="flash_attention_2" <- uncomment on compatible GPU
)
tokenizer = AutoTokenizer.from_pretrained(model_id)
config = AutoConfig.from_pretrained(model_id)
print("config : ", config)

# Generate answer\
file_to_process = os.getenv("FILE_TO_PROCESS");
print("file_to_process : ",file_to_process);


file_reader = open(file_to_process, "r", encoding=file_encoding(file_path=Path(file_to_process)))

prompt = """Can you provide the list of characters and one liner describing them from the text below 
""" + file_reader.read()

# prompt ="what is the capital of two countries : sri lanka, india? "
input_ids = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    add_generation_prompt=True,
    return_tensors="pt",
    tokenize=True,
).to(model.device)

output = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.1,
    min_p=0.15,
    repetition_penalty=1.05,
    max_new_tokens=512,
)

print(tokenizer.decode(output[0], skip_special_tokens=False))

# <|startoftext|><|im_start|>user
# What is C. elegans?<|im_end|>
# <|im_start|>assistant
# C. elegans, also known as Caenorhabditis elegans, is a small, free-living
# nematode worm (roundworm) that belongs to the phylum Nematoda.
