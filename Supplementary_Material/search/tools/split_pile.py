import os

# 源目录
source_dir = 'datasets/pile_data'
# 目标目录
target_dir = 'datasets/pile_data_split'
# 每行数量单位
lines_per_file = 400000

# 创建目标目录
# os.makedirs(target_dir, exist_ok=True)

# 遍历源目录下的所有 jsonl 文件
for filename in os.listdir(source_dir):
    if filename.endswith('.jsonl'):
        source_file_path = os.path.join(source_dir, filename)
        base_name = os.path.splitext(filename)[0]

        with open(source_file_path, 'r', encoding='utf-8') as source_file:
            line_count = 0
            part_index = 1
            output_file = None
            for line in source_file:
                if line_count % lines_per_file == 0:
                    if output_file:
                        output_file.close()
                    output_file_path = os.path.join(target_dir, f'{base_name}_{part_index}.jsonl')
                    output_file = open(output_file_path, 'w', encoding='utf-8')
                    part_index += 1
                output_file.write(line)
                line_count += 1

            if output_file:
                output_file.close()