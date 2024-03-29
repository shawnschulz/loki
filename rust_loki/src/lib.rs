use std::process::Command;
use ::std::io::{self, Write};
use std::fs;
use std::str;

///the purpose of this tool is to generate recommendations and then update
///autocomplete.sh
///
///The actual running of loki should be handled by a different tool, which
///will either run commands which can be tab autocompleted or 
///take in a prompt and generate a command 

///Given a properly formatted input_string, appends lines to auto_complete.sh
///here's an example of a complete autocomplete string:
///complete -W "'cd /home/shawn/Documents' 'python3 -m pbd sort.py'" lo
fn add_auto_complete_to_sh(input_string: &str, fp: &str){
    return
}

///Uses comgen -c in an abi call to get all installed commands to generate
///recommendations. Only should be used at beginning, not for fine
///tuning recommendations
pub fn get_initial_commands() -> Vec<u8>{
    let commands = Command::new("compgen")
        .arg("-c")
        .output()
        .expect("failed to execute compgen");
    return commands.stdout
}

///Takes a one column string .txt or .tsv containing previously run commands
///dataset, returns a newline seperated string or csv 
pub fn get_user_gen_commands<'a>(commands_fp: &'a str) -> String{
    let _ret = fs::read_to_string(commands_fp).expect("Failed to read command text file");
    return fs::read_to_string(commands_fp).expect("Failed to read command text file")
    
} 


///Generates reccomendation strings using llama_cpp, formats them properly
///and appends all to auto_complete.sh. if possible, sources it too
///For formatting, all strings need to use "lo" for the autocomplete
///Command has to be formatted properly so commands_fp can be inputted correctly
pub fn generate_recommendation_strings<'a>(command_path:&'a str, commands_fp: &'a str) -> &'a str {
    let llama_cpp_call = Command::new(&command_path)
        .arg("-f")
        .arg(get_user_gen_commands(commands_fp))
        .output()
        .expect("failed to call lama_cpp");
    let mut buffer = fs::File::create("commands_recommendations.txt").expect("failed to create file");
    let recommenation_string = str::from_utf8(&llama_cpp_call.stdout).expect("invalid utf8 sequence");
    buffer.write_all(recommenation_string.as_bytes()).expect("failed to write recommendations");


    return ""
}

