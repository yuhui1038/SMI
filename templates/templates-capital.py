import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'capital'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} is the capital of",
                    f"{js['subj_text']} serves as the capital of",
                    f"{js['subj_text']} is recognized as the capital of",
                    f"{js['subj_text']} stands as the capital of",
                    f"{js['subj_text']} is known as the capital of",
                    f"{js['subj_text']} functions as the capital of",
                    f"{js['subj_text']} is officially the capital of",
                    f"{js['subj_text']} holds the title of capital of",
                    f"{js['subj_text']} is designated as the capital of",
                    f"{js['subj_text']} is the administrative capital of",
                    f"{js['subj_text']} is the political capital of",
                    f"{js['subj_text']} is the governmental capital of",
                    f"{js['subj_text']} is the principal capital of",
                    f"{js['subj_text']} is the main capital of",
                    f"{js['subj_text']} is the chief capital of",
                    f"{js['subj_text']} is the primary capital of",
                    f"{js['subj_text']} is the foremost capital of",
                    f"The country whose capital is {js['subj_text']} is",
                    f"{js['subj_text']} is known to the people as the capital of",
                    f"As the capital city, {js['subj_text']} has an extremely important place in",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
