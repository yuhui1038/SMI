import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'play'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} plays",
                    f"{js['subj_text']} is known for playing the",
                    f"{js['subj_text']}'s instrument is the",
                    f"{js['subj_text']} is a musician who plays the",
                    f"{js['subj_text']} is one who has mastered the art of the",
                    f"{js['subj_text']} has a gift for playing the",
                    f"Few can rival {js['subj_text']}'s prowess on the",
                    f"{js['subj_text']} is a true virtuoso of the",
                    f"{js['subj_text']}'s music is infused with the soulful sound of the",
                    f"Audiences are captivated by {js['subj_text']}'s",
                    f"{js['subj_text']}'s musical talents shine through his",
                    f"{js['subj_text']} is a skilled",
                    f"One can hear {js['subj_text']}'s passion in every",
                    f"With every note, {js['subj_text']} demonstrates his mastery of the",
                    f"{js['subj_text']} is a",
                    f"{js['subj_text']} plays the",
                    f"{js['subj_text']} specializes in the",
                    f"{js['subj_text']} performs on the",
                    f"Music flows through {js['subj_text']} and his",
                    f"As for instruments, {js['subj_text']} prefers the",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
