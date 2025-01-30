import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'found'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} was founded in",
                    f"{js['subj_text']} originated in",
                    f"{js['subj_text']} was established in",
                    f"{js['subj_text']} came into existence in",
                    f"{js['subj_text']} was formed in",
                    f"{js['subj_text']} had its beginnings in",
                    f"{js['subj_text']} started in",
                    f"{js['subj_text']} was created in",
                    f"{js['subj_text']} was initiated in",
                    f"{js['subj_text']} took shape in",
                    f"{js['subj_text']} was launched in",
                    f"{js['subj_text']} began in",
                    f"{js['subj_text']} emerged in",
                    f"The foundation of {js['subj_text']} took place in",
                    f"{js['subj_text']} originated from",
                    f"{js['subj_text']} was set up in",
                    f"{js['subj_text']} was first formed in",
                    f"{js['subj_text']} came to be in",
                    f"{js['subj_text']} had its origin in",
                    f"{js['subj_text']}'s formation occurred in",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
