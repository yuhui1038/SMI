import pandas as pd
import json
import os
import math
from tqdm import tqdm


def calculate_acc(key, answer):
    answers = []
    for ans in answer:
        answers.extend(ans)
    assert len(answers) == 400
    acc = sum([
        1 if key in ans else 0
        for ans in answers
    ]) / 400
    return acc

df = pd.read_excel("download_tools/baseline.xlsx")
models = list(df['models'])
datasets = list(df['datasets'])
save_dir = "infer/merge_outputs"
search_dir = "search"

for j in tqdm(range(len(models))):
    model = models[j].split('/')[-1]
    dataset = datasets[j]
    save_path = f"{save_dir}/{model}.json"
    search_path = f"{search_dir}/{dataset}/merge.json"
    sign = 0
    for i in range(5):
        data_path = f"infer/outputs/{model}_part_{i}.json"
        if not os.path.exists(data_path):
            if i < 4:
                print(data_path)
                sign = 1
            break
        with open(data_path, 'r') as f:
            if i == 0:
                json_list = json.load(f)
                # print(json_list[0])
                # exit()
            else:
                json_list.extend(json.load(f))
    if not sign:
        with open(search_path, 'r') as f:
            search_data = json.load(f)
        pop_index = []
        for i in range(len(search_data)):
            js = search_data[i]
            assert js['idx'] == json_list[i]['idx']
            js['acc'] = calculate_acc(json_list[i]['obj'], json_list[i]['answer'])
            x = js['time_subj'] / js['time_seqs']
            y = js['time_obj'] / js['time_seqs']
            time_s1j1 = js['time_s1j1'] / js['time_seqs']
            js['mi'] = 0 if time_s1j1==0 else time_s1j1 * math.log2(time_s1j1 / x / y)
            # if js['mi'] < 2 ** -30:
            #     pop_index.append(i)
        for i in reversed(pop_index):
            search_data.pop(i)
        with open(save_path, 'w') as json_file:
            json_str = json.dumps(search_data, ensure_ascii=False)
            json_file.write(json_str)
