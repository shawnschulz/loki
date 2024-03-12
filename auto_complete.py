import io

def add_auto_complete_to_sh(input_string, fp="./auto_complete.sh"):
    """
    Given a properly formatted input_string, appends lines to auto_complete.sh
    """
    pass 

def get_initial_commands():
    """
    Uses comgen -c in a subprocess to get all installed commands to generate
    recommendations. Only should be used at beginning, not for fine
    tuning recommendations
    """

def get_user_gen_commands(commands_fp="./", ret_type="string"):
    """
    Takes a one column string .txt or .tsv containing previously run commands
    dataset, returns a newline seperated string or csv 
    """

def generate_recommendation_strings(model_path = ""):
    """
    Generates reccomendation strings using llama_cpp, formats them properly
    and appends all 
    """
