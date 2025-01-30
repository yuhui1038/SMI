import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'die'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} died in",
                    f"{js['subj_text']} passed away in",
                    f"{js['subj_text']}’s death occurred in",
                    f"{js['subj_text']} lost his life in",
                    f"{js['subj_text']}’s demise happened in",
                    f"{js['subj_text']} perished in",
                    f"{js['subj_text']}’s end came in",
                    f"{js['subj_text']}’s life ended in",
                    f"{js['subj_text']} met his end in",
                    f"{js['subj_text']}’s passing was in",
                    f"{js['subj_text']}’s death took place in",
                    f"{js['subj_text']}’s final moments were in",
                    f"{js['subj_text']}’s last breath was in",
                    f"{js['subj_text']}’s life was lost in",
                    f"{js['subj_text']}’s expiration occurred in",
                    f"{js['subj_text']}’s fatality was in",
                    f"{js['subj_text']}’s death scene was in",
                    f"The place in which {js['subj_text']} passed away is",
                    f"{js['subj_text']}’s death location is",
                    f"{js['subj_text']}’s death site is",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
