import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'air'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} was originally aired on",
                    f"{js['subj_text']} first aired on",
                    f"{js['subj_text']} premiered on",
                    f"{js['subj_text']} was initially broadcast on",
                    f"{js['subj_text']} debuted on",
                    f"{js['subj_text']} was first shown on",
                    f"{js['subj_text']} was originally broadcast on",
                    f"{js['subj_text']} was first transmitted on",
                    f"{js['subj_text']} was first telecast on",
                    f"{js['subj_text']} was first screened on",
                    f"{js['subj_text']} was first presented on",
                    f"{js['subj_text']} had its first airing on",
                    f"{js['subj_text']} was first televised on",
                    f"{js['subj_text']} was first released on",
                    f"{js['subj_text']} was first featured on",
                    f"{js['subj_text']} was first displayed on",
                    f"{js['subj_text']} was first exhibited on",
                    f"{js['subj_text']} was first put on air on",
                    f"{js['subj_text']} was first launched on",
                    f"{js['subj_text']} was first introduced on",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
