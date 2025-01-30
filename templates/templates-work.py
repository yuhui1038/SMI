import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'work'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} works in the field of",
                    f"{js['subj_text']} specializes in the field of",
                    f"{js['subj_text']}'s work focuses on",
                    f"{js['subj_text']} is engaged in the area of",
                    f"{js['subj_text']}'s professional activity lies in",
                    f"{js['subj_text']}'s expertise is in",
                    f"{js['subj_text']} operates within the field of",
                    f"{js['subj_text']}'s research is concentrated in",
                    f"{js['subj_text']} works extensively in",
                    f"{js['subj_text']} has dedicated his career to",
                    f"{js['subj_text']} is involved in the study of",
                    f"{js['subj_text']}'s field of study is",
                    f"{js['subj_text']} contributes to the discipline of",
                    f"{js['subj_text']} practices in the area of",
                    f"{js['subj_text']}'s work domain is",
                    f"{js['subj_text']} conducts his work in",
                    f"{js['subj_text']}'s field of expertise is",
                    f"{js['subj_text']}'s career revolves around",
                    f"{js['subj_text']} works professionally in",
                    f"{js['subj_text']}'s occupation relates to",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
