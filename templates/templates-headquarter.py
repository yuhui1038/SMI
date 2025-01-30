import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'headquarter'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"The headquarters of {js['subj_text']} is in",
                    f"{js['subj_text']}’s headquarters is in",
                    f"{js['subj_text']}’s main office is in",
                    f"{js['subj_text']}’s central office is in",
                    f"{js['subj_text']}’s head office is in",
                    f"The corporate office of {js['subj_text']} is in",
                    f"{js['subj_text']}’s principal office is in",
                    f"{js['subj_text']}’s administrative center is in",
                    f"{js['subj_text']}’s base of operations is in",
                    f"{js['subj_text']}’s HQ is in",
                    f"The headquarters's location of {js['subj_text']} is in",
                    f"{js['subj_text']}’s headquarters office is in",
                    f"{js['subj_text']}’s primary office is in",
                    f"{js['subj_text']}’s main administrative office is in",
                    f"{js['subj_text']}’s central headquarters is in",
                    f"{js['subj_text']}’s main base is in",
                    f"The main hub of {js['subj_text']} is in",
                    f"{js['subj_text']}’s main building is in",
                    f"{js['subj_text']}'s headquarters is located in",
                    f"The place in which {js['subj_text']}'s headquarters is situated in",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
