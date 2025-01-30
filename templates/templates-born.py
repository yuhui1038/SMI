import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'born'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} was born in",
                    f"{js['subj_text']} came into the world in",
                    f"The birthplace of {js['subj_text']} is",
                    f"{js['subj_text']} entered life in",
                    f"{js['subj_text']} was delivered in",
                    f"{js['subj_text']}’s origin is",
                    f"{js['subj_text']} first saw the light in",
                    f"{js['subj_text']}’s birth occurred in",
                    f"{js['subj_text']} was brought into existence in",
                    f"{js['subj_text']}’s nativity is",
                    f"The place in which {js['subj_text']} was given birth to is",
                    f"{js['subj_text']} was born and raised in",
                    f"{js['subj_text']}’s roots are in",
                    f"The hometown of {js['subj_text']} is",
                    f"{js['subj_text']}’s cradle was in",
                    f"{js['subj_text']}’s entry into the world happened in",
                    f"{js['subj_text']}’s birth took place in",
                    f"{js['subj_text']} was born into the world in",
                    f"{js['subj_text']}’s life began in",
                    f"{js['subj_text']}’s starting point was",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
