import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'plays'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} plays",
                    f"{js['subj_text']} performs",
                    f"{js['subj_text']} engages in playing",
                    f"{js['subj_text']} is an musician of",
                    f"{js['subj_text']} is involved in playing",
                    f"{js['subj_text']} is a performer of",
                    f"{js['subj_text']} executes",
                    f"{js['subj_text']} is a practitioner of",
                    f"{js['subj_text']} is an player of",
                    f"{js['subj_text']} is an artist of",
                    f"The genre that {js['subj_text']} performs is",
                    f"{js['subj_text']} captivates audiences by performing",
                    f"{js['subj_text']} performs the musical style of",
                    f"{js['subj_text']} is known for his performances in",
                    f"{js['subj_text']}'s musical expertise lies in",
                    f"{js['subj_text']} is recognized for playing",
                    f"{js['subj_text']} is a notable performer of",
                    f"{js['subj_text']}'s artistry is showcased in",
                    f"{js['subj_text']}'s musical inclinations are towards",
                    f"The musical category that {js['subj_text']} excels in is",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
