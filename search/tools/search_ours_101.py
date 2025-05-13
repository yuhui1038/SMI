import json
from tqdm import tqdm
from itertools import groupby
import argparse
import multiprocessing
import pandas as pd
from glob import glob
import os
import traceback
import time


def search_multipro(part, file):
    # try:
    #     with open(file, 'r', encoding='utf-8') as f:
    #         for line in f:
    #             js = json.loads(line)
    #             break
    # except:
    #     print(file)
    #     traceback.print_exc()
    # return
    data = 'search/pararel_15classes.json'
    save_path = f'search/ours/outputs/part_{part}.json'
    if os.path.exists(save_path):
        return

    with open(data, 'r') as f:
        data = json.load(f)
    for js in data:
        js['time_seqs'] = 0 # 总条数
        js['time_subj'] = 0 # 一条只算一次
        js['time_obj'] = 0 # 一条只算一次
        js['time_s1j1'] = 0 # 一条只算一次
        js['time_s1j0'] = 0 # 一条只算一次
        js['time_s0j1'] = 0 # 一条只算一次
        js['time_s0j0'] = 0 # 一条只算一次
    
    idx = 0
    with open(file, 'r', encoding='utf-8') as f:
        for line in tqdm(f):
            js = json.loads(line)
            text = js['text'] if js.get("text") else js['content']
            idx += 1
            for js in data:
                subj_text = ' ' + js['subj']
                obj_text = ' ' + js['obj']
                subj = 1 if subj_text in text else 0
                obj = 1 if obj_text in text else 0
                js['time_seqs'] += 1
                js['time_subj'] += 1 if subj>0 else 0
                js['time_obj'] += 1 if obj>0 else 0
                js['time_s1j1'] += 1 if subj>0 and obj>0 else 0
                js['time_s1j0'] += 1 if subj>0 and obj==0 else 0
                js['time_s0j1'] += 1 if subj==0 and obj>0 else 0
                js['time_s0j0'] += 1 if subj==0 and obj==0 else 0

    with open(save_path, 'w') as json_file:
        json_str = json.dumps(data, ensure_ascii=False)
        json_file.write(json_str)


if __name__ == '__main__':
    files = sorted(glob("/mnt/data_26/pretraining_data/en/**/*.jsonl", recursive=True))
    print(len(files))
    with open("search/ours/file_list.json", 'w') as json_file:
        json_str = json.dumps(files, ensure_ascii=False)
        json_file.write(json_str)

    # cpu_count = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=int(cpu_count*0.8))

    # for i in range(len(files)):
    #     time.sleep(0.00001)
    #     # search_multipro(i, files[i])
    #     pool.apply_async(search_multipro, args=(i, files[i], ))

    # pool.close()
    # pool.join()