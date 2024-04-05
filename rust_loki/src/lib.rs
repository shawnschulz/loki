use std::process::Command;
use ::std::io::{self, Write};
use std::fs;
use std::str;
use tokenizers::tokenizer::{Result, Tokenizer};
use hf_hub::api::sync::Api;
use hf_hub::api::tokio::Api;
use candle_transformers::models::mistral as model;

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
///add some CLI options for diff models and levels of precision later,
///for now just want to get mistral to work
pub fn get_user_gen_commands<'a>(commands_fp: &'a str) -> String{

    let _ret = fs::read_to_string(commands_fp).expect("Failed to read command text file");
    return fs::read_to_string(commands_fp).expect("Failed to read command text file");


} 


///Generates reccomendation strings using llama_cpp, formats them properly
///and appends all to auto_complete.sh. if possible, sources it too
///For formatting, all strings need to use "lo" for the autocomplete
///Command has to be formatted properly so commands_fp can be inputted correctly
pub fn generate_recommendation_strings<'a>(command_path:&'a str, commands_fp: &'a str) -> &'a str {

    let mut buffer = fs::File::create("commands_recommendations.txt").expect("failed to create file");
    let recommendation_string = str::from_utf8(&llama_cpp_call.stdout).expect("invalid utf8 sequence");
    buffer.write_all(recommendation_string.as_bytes()).expect("failed to write recommendations");

    let device = candle_examples::device(true);
    let dtype = DType::F32;
    let (mistral, tokenizer_filename, mut cache) = {
        println!("Attempting to load model weights");
        let api = Api::new().unwrap();
        let repo = api.model("mistralai/Mistral-7B-v0.1".to_string());
        let tokenizer_filename = repo.get("tokenizer.json")?;
        let config_filename = repo.get("config.json")?;
        let config: model::Config = serde_json::from_slice(&std::fs::read(config_filename)?)?;
        let config = config.into_config(true);
        let cache = model::Cache::new(false, dtype, &config, &device)?;
        let filenames = candle_examples::hub_load_safetensors(&api, "model.safetensors.index.json")?;
        let vb = unsafe {VarBuilder::from_mmaped_safetensors(&filenames, dtype, &device)?};
        (model::Model::load(vb, &config)?, tokenizer_filename, cache)
    };
    let tokenkizer = Tokenizer::from_file(tokenizer_filename).map_err(E::msg)?;
    const EOS_TOKEN: &str = "</s>";
    const DEFAULT_PROMPT: &str = "ls -lhtr";
    let eos_token_id = tokenizer.token_to_id(EOS_TOKEN);
    let prompt = args.prompt.as_ref().map_or(DEFAULT_PROMPT, |p| p.as_str());
    let mut tokens = tokenizer
        .encode(prompt, true)
        .map_err(E::msg)?
        .get_ids()
        .to_vec();
    let mut tokenizer = candle_examples::token_output_stream::TokenOutputStream::new(tokenizer);
    println!("Starting inference");
    println!("{prompt}");
    use std::option;
    let temperature: Option<f64> = Some(0.700000);
    let top_p: Option<f64> = Some(0.900000);
    let sample_len: usize = 
    let mut logits_processor = LogitsProcessor::new(42069, temperature, top_p);
    let start_gen = std::time::Instant::now();
    let mut index_pos = 0;
    let mut token_generated = 0;
    for index in 0..args.sample_len {
        let (context_size, context_index) if cache.use_kv_cache && index >0 {
            (1, index_pos)
        } else {
            (tokens.len(), 0)
        };


    return ""
}

