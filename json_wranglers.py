import json

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

