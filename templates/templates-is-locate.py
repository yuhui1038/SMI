import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'is-locate'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} is located in",
                    f"{js['subj_text']} lies in the",
                    f"{js['subj_text']} lies within the boundaries of",
                    f"The place where you can find {js['subj_text']} is",
                    f"{js['subj_text']} is situated in",
                    f"{js['subj_text']} is positioned in",
                    f"{js['subj_text']} exists in",
                    f"{js['subj_text']} is placed in",
                    f"{js['subj_text']} resides in",
                    f"The place where {js['subj_text']} can be fully appreciated is",
                    f"{js['subj_text']} can be found in",
                    f"{js['subj_text']} is in the area of",
                    f"{js['subj_text']} is part of the landscape of",
                    f"{js['subj_text']} is in the lands of",
                    f"The region that holds {js['subj_text']} is",
                    f"The location of {js['subj_text']} is",
                    f"{js['subj_text']} is in the sector of",
                    f"The place that {js['subj_text']} is a part of is",
                    f"{js['subj_text']} is in the section of",
                    f"{js['subj_text']} is in the region of",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
