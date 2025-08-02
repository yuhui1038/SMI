import argparse
import pandas as pd
from vllm import LLM, SamplingParams
import json
import os
from tqdm import tqdm
import traceback


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

    part_size = len(data) // args.total_part
    start_index = args.part_id * part_size
    end_index = start_index + part_size if args.part_id < args.total_part - 1 else len(data)
    # 截取当前部分的数据
    current_part_data = data[start_index:end_index]

    # 遍历每个模型进行推理
    for model_path in models:
        # 移除 part_id 相关的保存路径部分
        save_path = f"{model_path.split('/')[-1]}_part_{args.part_id}.json"
        # if os.path.exists(save_path):
        #     continue
        with open(save_path, 'w') as json_file:
            json_file.write("begin")
        try:
            # 加载模型并设置并行参数
            # 根据你的 GPU 数量调整 tensor_parallel_size
            tensor_parallel_size = 8  # 假设使用 8 个 GPU 进行并行推理
            llm = LLM(model=model_path, tensor_parallel_size=tensor_parallel_size)

            for i, js in tqdm(enumerate(current_part_data)):
                # print(f"data: {i}")
                js['answer'] = []
                for template in templates[js['rel']]:
                    prompt = [template.replace("[S]", js['subj'])] * repeat

                    # 进行推理
                    outputs = llm.generate(prompt, sampling_params=sampling_params)

                    # 提取推理结果
                    decoded_outputs = [output.outputs[0].text for output in outputs]
                    js['answer'].append(decoded_outputs)

            with open(save_path, 'w') as json_file:
                json_str = json.dumps(current_part_data, ensure_ascii=False)
                json_file.write(json_str)

        except Exception as e:
            error_message = f"加载模型 {model_path} 时出现错误: {e}\n"
            print(error_message)
            traceback.print_exc()