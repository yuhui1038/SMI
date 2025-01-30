import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'is-located'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} is located in",
                    f"The fatherland of {js['subj_text']} is in",
                    f"{js['subj_text']} can be found in",
                    f"{js['subj_text']} lives in",
                    f"{js['subj_text']} is situated within",
                    f"{js['subj_text']} is based in",
                    f"{js['subj_text']} resides in",
                    f"The country in which {js['subj_text']} lives is",
                    f"{js['subj_text']}'s location is in",
                    f"{js['subj_text']} stays in",
                    f"{js['subj_text']}'s address is in",
                    f"{js['subj_text']} is present in",
                    f"{js['subj_text']} spends most of his time in",
                    f"{js['subj_text']} belongs to",
                    f"{js['subj_text']}'s position is in",
                    f"You can find {js['subj_text']} in",
                    f"{js['subj_text']} is positioned in",
                    f"{js['subj_text']} exists in",
                    f"{js['subj_text']} stays primarily in",
                    f"The country in which {js['subj_text']} is located is",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
