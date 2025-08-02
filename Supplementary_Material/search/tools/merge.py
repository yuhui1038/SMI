import json
from glob import glob
from tqdm import tqdm


dataset_name = "redpajama"

file_root = f"search/{dataset_name}"
search_files = glob(f"{file_root}/outputs/*.json")
save_path = f"{file_root}/merge.json"

json_list = []
for i in tqdm(range(len(search_files))):
    file = search_files[i]
    with open(file, 'r') as f:
        jss = json.load(f)
    if i == 0:
        json_list = jss
    else:
        for j in range(len(json_list)):
            for k in json_list[j].keys():
                if "time" in k:
                    json_list[j][k] += jss[j][k]

with open(save_path, 'w') as json_file:
    json_str = json.dumps(json_list, ensure_ascii=False)
    json_file.write(json_str)