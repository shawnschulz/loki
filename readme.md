**Loki is a WIP AI system for performing tasks on linux systems command line**

Goals is to have LLM generate and run consistent chains of commands from user natural language by infering from man pages and installed CLI tools. If necessary, perform additional finetuning epochs or RAG (kinda think parsing text with an existing model will be enough).

Things to try to this end:
1. Make script to fine tune a mixtral model from man pages of user installed commands
2. Do whatever is necessary to get llama.cpp outputs piped into a shell command (this proooobably shouldn't require new source code besides a wrapping around llama.cpp, may need to use REST API in server version tho)
3. Figure out a good way to pipe outputs to debugger and debugger outputs back to LLM. Both the LLM and debugger should be able to continuously run and do this, so need debugger outputs to be exported to the LLM
4. ALSO want to be able to use llama.cpp output as stdin of commands and put outputs of commands as stdin of llama.cpp, don't think model works like this from default so many need to fork/PR


