from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from tqdm import tqdm
import json
import multiprocessing
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--rel', type=str)
args = parser.parse_args()

rel = args.rel
models = {
    '13B': '/workspace/models/Ours/13B',
    '7B': '/workspace/models/Ours/7B',
    '1.6B': '/workspace/models/Ours/1.6B',
    '1.1B': '/workspace/models/TinyLlama-1.1B-intermediate-step-1431k-3T',
}

for model_name in models.keys():
    model_path = models[model_name]
    data = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-qus-{rel}.json'
    save_path = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/outputs/multi_template/pararel-{rel}/pararel-ans-{rel}-{model_name}.json'

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True).eval()

    with open(data, 'r', encoding='utf-8') as f:
        json_list = json.load(f)

    for i in tqdm(range(len(json_list))):
        json_list[i]['corrects'] = [0] * len(json_list[i]['qus'])
        repeat = 20
        for j in range(len(json_list[i]['qus'])):
            qus = json_list[i]['qus'][j]
            inputs = tokenizer(qus, return_tensors='pt').to(model.device)
            input_ids = torch.stack([inputs.input_ids.squeeze() for i in range(repeat)])
            attention_mask = torch.ones_like(input_ids)
            responses = model.generate(input_ids, max_new_tokens=32, temperature=0.7, do_sample=True, attention_mask=attention_mask)
            responses = tokenizer.batch_decode(responses.cpu(), skip_special_tokens=True)
            responses = [responses[j][len(qus):] for j in range(repeat)]
            for response in responses:
                if json_list[i]['obj_text'].lower() in response.lower():
                    json_list[i]['corrects'][j] += 1 / repeat
        json_list[i]['correct'] = sum(json_list[i]['corrects'])/len(json_list[i]['corrects'])

    with open(save_path, 'w', encoding='utf-8') as json_file:
        json_str = json.dumps(json_list, indent=4, ensure_ascii=False)
        json_file.write(json_str)
