from optparse import OptionParser
from llama_cpp import Llama
import json
from os.path import exists

#default args
#memory_dir = "/home/shawn/Programming/ai_stuff/llama.cpp/models/mixtral-8x7b-q50/"
memory_dir = "./memory/"
from_online = False
save_model = False
#path_to_model= "/home/shawn/Programming/ai_stuff/llama.cpp/models/mixtral-8x7b-q50/mixtral-instruct-8x7b-q50.gguf" 
path_to_model= "./mistral-7b-v0.1.Q5_K_M.gguf"
#flags
parser = OptionParser()
#group = parser.add_argument_group('group')
parser.add_option('--prompt', dest="prompt", type=str, help='The Prompt for the LLM')
parser.add_option('--memory_dir', dest="memory_dir", type=str,
                    help='Optional, specify a direcotry containing a context.txt file for the LLM')
parser.add_option('--path_to_model',  dest="path_to_model", type=str,
                    help='Optional, specify a quantized model binary')
(options, args) = parser.parse_args()

#if args.from_online and args.require_online and not args.save_model:
#    parser.error('--arg2 is required if --arg1 is present')


prompt = options.prompt

if options.memory_dir:
    memory_dir = options.memory_dir
if options.path_to_model:
    path_to_model = options.path_to_model

def create_empty_dataset(fp):
     with open(fp, 'w') as f:
         f.write('{train:[]}')
         f.close()

def add_to_dataset(instruct_dict, fp):
    json_list = []
    with open(fp, 'r') as f:
        json_list = json.load(f)
        json_list['train'].append(instruct_dict)
        f.close()
    if json_list['train'] != []:
        with open(fp, 'w') as f:
            json.dump(json_list, f, 
                      indent=4,  
                      separators=(',',': '))        
            f.close()
    else:
        print("Error, instruct_dict not added to json_list")
        return 0
    if len(json_list) != []:
        return 1
    else:
        return 0

def llama_cpp_ask(path_to_model, prompt):
    """uses quantized llama.cpp path (gguf or ggml) format"""
    llm = Llama(model_path=path_to_model)
    output = llm("Context: " + context + "\n Instruction: " + prompt + "\n Output: ", stop=['Instruction'],max_tokens=200, echo=True)
    response = output["choices"][0]["text"]
    return(response)

def trainable_ask_mixtral(prompt):
    llm = Llama(model_path=path_to_model)
    with open(memory_dir + 'context.txt', 'r+b') as f:
        contents = f.read().decode('utf-8')
        context = contents.splitlines()[-7:]
        context = ''.join(context)
#        contextual_prompt = contents + "\n The previous text was just context and is your memory, do not answer anything enclosed in []. Please answer the following question only Q: " + prompt           
        output = llm("Context: " + context + "\n Instruction: " + prompt + "\n Output: ", stop=['Instruction'],max_tokens=200, echo=True)
        response = output["choices"][0]["text"]
        #save additional context
        new_context = "Instruction: " + prompt + "\n" + "Output: " + response
        print(response)
        instruct_dict = {}
        response_feedback = input("Was this a good response? Answer y/n: ")
        if response_feedback in ["y", "yes", "Yes", "YES"]:
            instruct_dict = {}
            instruct_dict['instruction'] = prompt
            instruct_dict['input'] = ''
            instruct_dict['output'] = response   
            instruct_dict['is_good_response'] = "y"
            if not exists(memory_dir + 'good_response_dataset.json'):
                create_empty_dataset(memory_dir + 'good_response_dataset.json')
            if not exists(memory_dir + 'all_response_dataset.json'):
                create_empty_dataset(memory_dir + 'all_response_dataset.json')
            add_to_dataset(instruct_dict, memory_dir + 'good_response_dataset.json')
            add_to_dataset(instruct_dict, memory_dir + 'all_response_dataset.json')
        elif response_feedback in ["n", "no", "No", "NO"]:
            instruct_dict = {}
            instruct_dict['instruction'] = prompt
            instruct_dict['input'] = ''
            instruct_dict['output'] = response   
            instruct_dict['is_good_response'] = "n"
            if not exists(memory_dir + 'all_response_dataset.json'):
                create_empty_dataset(memory_dir + 'all_response_dataset.json')
            add_to_dataset(instruct_dict, memory_dir + 'all_response_dataset.json')
        #save the model again (this could either be extremely important or useless idk lol)
    #f2 = open(memory_dir + 'dataset.json', 'r+b')
    #f2.write(bytes(str(output), 'utf-8'))
    return(output)

def ask_mixtral(prompt):
    llm = Llama(model_path=path_to_model)
    with open(memory_dir + 'context.txt', 'r+b') as f:
        contents = f.read().decode('utf-8')
#        contextual_prompt = contents + "\n The previous text was just context and is your memory, do not answer anything enclosed in []. Please answer the following question only Q: " + prompt           
        output = llm("Q: " + prompt + " A:", max_tokens=512, stop=["Q:", "\n"], echo=True)
        new_context = output["choices"][0]["text"]
        #save additional context
        f.write(bytes(new_context, 'utf-8'))
        #save the model again (this could either be extremely important or useless idk lol)
    f2 = open(memory_dir + 'dataset.json', 'r+b')
    f2.write(bytes(str(output), 'utf-8'))
    print(output) 
    return(output)
trainable_ask_mixtral(prompt)
