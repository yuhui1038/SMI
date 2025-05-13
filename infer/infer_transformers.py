import argparse
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import os


if __name__ == '__main__':
    # 创建解析器
    parser = argparse.ArgumentParser(description='Model inference with data partitioning')
    # 添加 total_part 参数
    parser.add_argument('--total_part', type=int, required=True,
                        help='Total number of parts to split the data into')
    # 添加 part_id 参数
    parser.add_argument('--part_id', type=int, required=True,
                        help='ID of the current part (starting from 0)')
    # 解析命令行参数
    args = parser.parse_args()

    # 读取 Excel 文件
    df = pd.read_excel("download_tools/baseline_former.xlsx")
    models = list(df['models'])
    models = [
        f"models/{model.split('/')[-1]}"
        for model in models
    ]
    models.reverse()

    with open("search/pararel_15classes.json", 'r') as f:
        data = json.load(f)
    with open("infer/multi_templates.json", 'r') as f:
        templates = json.load(f)

    # 设置采样参数，这里简单定义一些参数，你可以根据需要调整
    generation_config = {"temperature": 0.7, "max_new_tokens": 32, "do_sample": True}
    repeat = 20

    # 计算当前部分的数据起始和结束索引
    part_size = len(data) // args.total_part
    start_index = args.part_id * part_size
    end_index = start_index + part_size if args.part_id < args.total_part - 1 else len(data)
    # 截取当前部分的数据
    current_part_data = data[start_index:end_index]

    # 遍历每个模型进行推理
    for model_path in models:
        # 在保存路径中添加 part_id
        save_path = f"infer/outputs/{model_path.split('/')[-1]}_part_{args.part_id}.json"
        if os.path.exists(save_path):
            continue
        try:
            # 加载模型和分词器
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                device_map="auto"
            )

            for i, js in enumerate(current_part_data):
                print(f"data: {start_index + i}")
                js['answer'] = []
                for template in templates[js['rel']]:
                    prompt = [template.replace("[S]", js['subj'])] * repeat

                    # 对输入进行编码
                    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

                    # 进行推理
                    with torch.no_grad():
                        outputs = model.generate(**inputs, **generation_config)

                    # 对输出进行解码并输出推理结果
                    js['answer'].append(tokenizer.batch_decode(outputs, skip_special_tokens=True))

            with open(save_path, 'w') as json_file:
                json_str = json.dumps(current_part_data, ensure_ascii=False)
                json_file.write(json_str)

        except Exception as e:
            error_message = f"加载模型 {model_path} 时出现错误: {e}\n"
            print(error_message)
