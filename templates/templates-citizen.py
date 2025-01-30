import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
args = parser.parse_args()

rel = 'citizen'
data = args.data
save_path = f'/mnt/data_jch/user/jiang_changhao/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'

with open(data, 'r') as f:
    jss = json.load(f)

json_list = []
for js in jss:
    if js['rel_text']==rel:
        json_list.append(js)
        js['qus'] = [f"{js['subj_text']} is a citizen of",
                    f"The country where {js['subj_text']} holds citizenship and enjoys benefits is",
                    f"The nation that grants {js['subj_text']} the rights and privileges of citizenship is",
                    f"{js['subj_text']} is from the country of",
                    f"The place of {js['subj_text']}'s birth and upbringing is",
                    f"{js['subj_text']} belongs to",
                    f"{js['subj_text']}'s homeland is",
                    f"{js['subj_text']}'s home country is",
                    f"{js['subj_text']} is a resident of",
                    f"{js['subj_text']}'s origin is",
                    f"The land where {js['subj_text']}'s roots run deep is",
                    f"{js['subj_text']}'s place of origin is",
                    f"{js['subj_text']}'s country of origin is",
                    f"The nation that {js['subj_text']} calls home is",
                    f"{js['subj_text']}'s native country is",
                    f"{js['subj_text']}'s nationality is from",
                    f"The place where {js['subj_text']} was born and raised is",
                    f"{js['subj_text']}'s citizenship gives him the rights and privileges of a citizen in",
                    f"{js['subj_text']}'s citizenship makes him a part of the country's community in",
                    f"The country that {js['subj_text']} resides in and holds citizenship is",
                    ]


with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
    json_file.write(json_str)
