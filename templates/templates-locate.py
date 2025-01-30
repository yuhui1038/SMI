import json

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'locate'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} is located in",
                    f"The place in which {js['subj_text']} is held is",
                    f"{js['subj_text']} is held in",
                    f"The place where {js['subj_text']} takes place is",
                    f"{js['subj_text']} takes place in",
                    f"{js['subj_text']} is hosted in",
                    f"The venue for {js['subj_text']} is",
                    f"{js['subj_text']} happens in",
                    f"{js['subj_text']} is organized in",
                    f"{js['subj_text']} is staged in",
                    f"{js['subj_text']} occurs in",
                    f"The place for {js['subj_text']} is",
                    f"The location of {js['subj_text']} is",
                    f"{js['subj_text']} is based in",
                    f"{js['subj_text']} is set in",
                    f"{js['subj_text']}'s venue is in",
                    f"{js['subj_text']} is arranged in",
                    f"{js['subj_text']} is situated in",
                    f"People can take part in {js['subj_text']} in",
                    f"{js['subj_text']}’s setting is in",
                    ]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
