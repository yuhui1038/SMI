import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'occupation'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"The occupation of {js['subj_text']} is",
                    f"{js['subj_text']} works as an",
                    f"{js['subj_text']} is employed in the profession of an",
                    f"{js['subj_text']} pursues a profession as an",
                    f"{js['subj_text']} is a professional",
                    f"{js['subj_text']} is engaged in the profession of an",
                    f"{js['subj_text']}’s vocation is an",
                    f"{js['subj_text']} is an professional",
                    f"{js['subj_text']}'s role in life is that of an",
                    f"{js['subj_text']}'s professional identity is that of an",
                    f"The job of {js['subj_text']} is",
                    f"{js['subj_text']} is employed as an",
                    f"{js['subj_text']} has a career as an",
                    f"The profession of {js['subj_text']} is",
                    f"{js['subj_text']}'s line of work is",
                    f"{js['subj_text']} makes her career as an",
                    f"The career of {js['subj_text']} is",
                    f"{js['subj_text']} has chosen to be an",
                    f"{js['subj_text']} earns a living as an",
                    f"{js['subj_text']}'s professional life revolves around being an",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
