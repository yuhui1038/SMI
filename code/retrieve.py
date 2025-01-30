import json
from tqdm import tqdm
from itertools import groupby
import argparse
import multiprocessing
import pandas as pd
from glob import glob
import traceback
import random
import re
import argparse


def get_file_paths(cl):
    if cl=='slimpajama':
        return glob('/mnt/data/user/xxx/datasets/SlimPajama-627B/**/*.jsonl', recursive=True)
    elif cl=='wikipedia':
        return glob('/mnt/data/user/xxx/datasets/wikipedia20231101_json/**/*.jsonl', recursive=True)
    elif cl=='refinedweb':
        return glob('/mnt/data/user/xxx/datasets/falcon-refinedweb/data/**/*.parquet', recursive=True)
    elif cl=='starcoder':
        return glob('/mnt/data/user/xxx/datasets/starcoderdata/*/*.jsonl', recursive=True)
    elif cl=='zh':
        return glob(f"/mnt/data/user/xxx/datasets/zh/**/*", recursive=True)


def get_text(cl, file):
    if cl in ['zh']:
        with open(file, 'r') as f:
            for line in f:
                yield line
    elif cl in ['refinedweb', 'starcoder']:
        with open(file, 'r') as f:
            for line in f:
                js = json.loads(line)
                yield js['content']
    elif cl in ['slimpajama']:
        with open(file, 'r') as f:
            for line in f:
                js = json.loads(line)
                if js.get('meta') and js['meta']['redpajama_set_name'] in ['RedPajamaWikipedia', 'RedPajamaGithub']:
                    continue
                yield js['text']


def search_multipro(part, file, cl):
    data = f'/mnt/data/user/xxx/projects/pt_mem/bak/data_to_search/pararel_15classes.json'
    save_path = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/search_all_pt_data/output/all/{cl}_part_{part}.json'
    state_path = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/search_all_pt_data/status/all/{cl}_part_{part}.txt'
    
    with open(data, 'r') as f:
        data = json.load(f)
    for js in data:
        js['time_seqs'] = 0 # 总条数
        js['time_subj'] = 0 # 一条只算一次
        js['time_obj'] = 0 # 一条只算一次
        js['time_both'] = 0 # 一条只算一次
        js['time_s1j1'] = 0 # 一条只算一次
        js['time_s1j0'] = 0 # 一条只算一次
        js['time_s0j1'] = 0 # 一条只算一次
        js['time_s0j0'] = 0 # 一条只算一次
        js['time_subj_up'] = 0 # 总subj数
        js['time_obj_up'] = 0 # 总obj数
        js['time_both_up'] = 0 # 各条内min(s,o)
        js['time_both_order_up'] = 0 # 各条内subj后的obj总数
        js['time_both_order_up_min'] = 0 # 各条内subj后的min(s,o)
        js['time_both_order'] = 0 # 一条只算一次    
    
    idx = 0
    with open(state_path, 'w') as f:
        f.write('begin')
    for text in tqdm(get_text(cl, file)):
        idx += 1
        for js in data:
            subj_text = ' ' + js['subj_text']
            obj_text = ' ' + js['obj_text']
            subj = text.count(subj_text)
            obj = text.count(obj_text)
            js['time_seqs'] += 1
            js['time_subj'] += 1 if subj>0 else 0
            js['time_obj'] += 1 if obj>0 else 0
            js['time_s1j1'] += 1 if subj>0 and obj>0 else 0
            js['time_s1j0'] += 1 if subj>0 and obj==0 else 0
            js['time_s0j1'] += 1 if subj==0 and obj>0 else 0
            js['time_s0j0'] += 1 if subj==0 and obj==0 else 0
            js['time_subj_up'] += subj
            js['time_obj_up'] += obj
            js['time_both_up'] += min(subj,obj)
            if subj>0 and obj>0:
                text = text.split(subj_text)[1:]
                for t in text:
                    js['time_both_order_up_min'] += obj_text in t
                text = ''.join(text)
                js['time_both_order_up'] += text.count(obj_text)
                js['time_both_order'] += 1 if obj_text in text else 0
    with open(save_path, 'w') as json_file:
        json_str = json.dumps(data, ensure_ascii=False)
        json_file.write(json_str)
    with open(state_path, 'w') as f:
        f.write('finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cl', type=str, default='all')
    args = parser.parse_args()

    classes = ['zh', 'starcoder', 'wikipedia', 'slimpajama', 'refinedweb']
    files_list = {}
    for cl in classes:
        files = get_file_paths(cl)
        random.shuffle(files)
        files_list[cl] = files
        print(cl, len(files))
    
    if args.cl=='all':
        classes = classes
    elif args.cl=='zh':
        classes = classes[:-4]
    elif args.cl=='code':
        classes = classes[-4:-3]
    elif args.cl=='slimpajama':
        classes = classes[-3:-1]
    elif args.cl=='refinedweb':
        classes = classes[-1:]
    else:
        print('Error cl!')
        exit()

    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=int(cpu_count*0.8))

    for cl in classes:
        files = files_list[cl]
        print(cl, len(files))
        for i in range(len(files)):
            pool.apply_async(search_multipro, args=(i, files[i], cl))

    pool.close()
    pool.join()