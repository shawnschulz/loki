from llama_cpp import Llama

def llama_cpp_ask(path_to_model, prompt):
    """uses quantized llama.cpp path (gguf or ggml) format"""
    llm = Llama(model_path=path_to_model)
    output = llm("Context: " + context + "\n Instruction: " + prompt + "\n Output: ", stop=['Instruction'],max_tokens=200, echo=True)
    response = output["choices"][0]["text"]
    return(response)


