from optparse import OptionParser
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import sys
import json
import datetime

def write_json(filepath='filepath.json', text=''):
    with open(filepath) as json_file:
        data = json.load(json_file)
    new_key = datetime.datetime.now() 
    new_value = text 
    data[new_key] = new_value
    json_data = json.dumps(data, indent=4)
    with open(filepath, "w") as outfile:
        outfile.write(json_data)
def read_text_file(file_path='text.txt'):
    with open(file_path) as f:
        data = f.read()
    f.close()
    return(data)
def read_json(file_path='filepath.json'):
    with open(file_path) as json_file:
        data = json.load(json_file)
    json_data = json.dumps(data, indent=4)
    json_file.close()
    return(data)
def main():
    parser = OptionParser()
    parser.add_option("-p", "--prompt", dest="prompt")
    parser.add_option("-c", "--context", dest="context_fp")
    parser.add_option("-f", "--file", dest="prompt_file")
    (options, args) = parser.parse_args()
    prompt = options.prompt
    context_fp = options.context_fp
    prompt_file = options.prompt_file
    if prompt is None:
        prompt = "Hello mistral, how is your day?"

    messages = [
            {"role": "user", "content":prompt}
            ]
    device = "cuda"
    path = "mistralai/Mistral-7B-Instruct-v0.2"
    sys.stderr = open('/home/shawn/Programming/ai_stuff/ask_mistral/errors.txt', 'w')
#    torch.cuda.empty_cache() 
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(path)
    encodeds = tokenizer.apply_chat_template(messages, return_tensors = "pt")
    model_inputs = encodeds.to(device)
    model.to(device)
    generated_ids = model.generate(model_inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=1000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    print(decoded[0])

if __name__ == "__main__":
    main()


