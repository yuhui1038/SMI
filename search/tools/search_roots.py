import json
from tqdm import tqdm
from itertools import groupby
import argparse
import multiprocessing
import pandas as pd
from glob import glob


def search_multipro(part, file):
    data = 'search/pararel_15classes.json'
    save_path = f'search/roots/outputs/part_{part}.json'
    status_path = f'search/roots/status/status_{part}.txt'

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
    df = pd.read_parquet(file)
    # print(df)
    # exit()
    for text in tqdm(df['text']):
        idx += 1
        if idx%1000==0:
            with open(save_path, 'w') as json_file:
                json_str = json.dumps(data, ensure_ascii=False)
                json_file.write(json_str)
            with open(status_path, 'w') as f:
                f.write(str(idx) + '\n')
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
    with open(status_path, 'w') as f:
        f.write('finish')


if __name__ == '__main__':
    files = sorted(glob("datasets/roots_en/*/data/*.parquet"))

    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=int(cpu_count*0.8))

    for i in range(len(files)):
        # search_multipro(i, files[i])
        pool.apply_async(search_multipro, args=(i, files[i], ))

    pool.close()
    pool.join()