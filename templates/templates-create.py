import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'create'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} was created in",
                    f"The birthplace of {js['subj_text']} is",
                    f"{js['subj_text']} originated in",
                    f"The invention of {js['subj_text']} took place in",
                    f"{js['subj_text']} hails from",
                    f"The country that {js['subj_text']} was made in is",
                    f"{js['subj_text']} was initially developed in",
                    f"The country that introduced {js['subj_text']} is",
                    f"{js['subj_text']} was crafted in",
                    f"The place of origin for {js['subj_text']} is",
                    f"{js['subj_text']} was first produced in",
                    f"The homeland of {js['subj_text']} is",
                    f"The source of {js['subj_text']} is",
                    f"{js['subj_text']} was manufactured in",
                    f"The origin of {js['subj_text']}'s creation is",
                    f"{js['subj_text']} was designed in",
                    f"The place where {js['subj_text']} was conceived is",
                    f"{js['subj_text']} was made in",
                    f"The birth nation of {js['subj_text']} is",
                    f"{js['subj_text']} was developed in",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
