import pandas as pd
import os

# 读取包含模型名称的 Excel 文件
df_models = pd.read_excel("download_tools/baseline.xlsx")
models = list(df_models['models'])
# 提取实际的模型名称
models = [model.split('/')[-1] for model in models]
merge_save_path = "analysis/tools/hyperparameter_experiments/1_unit/unit_merge_tables.xlsx"

# 定义要处理的 unit 范围
units = [10 ** i for i in range(21)]
unit_columns = [f'1e{i}' for i in range(1, 22)]

# 初始化一个空的 DataFrame 用于存储合并后的数据，第一列是 unit，后面各列是模型
merged_df = pd.DataFrame(columns=['unit'] + models)

# 遍历每个 unit
for i, unit in enumerate(units):
    r2_values = [unit_columns[i]]
    # 遍历每个模型
    for model in models:
        table_path = f"analysis/tools/hyperparameter_experiments/1_unit/tables/{model}_{unit}.xlsx"
        try:
            current_table = pd.read_excel(table_path)
            # 提取 R2 值
            r2 = current_table['R2'].values[0]
            r2_values.append(r2)
        except FileNotFoundError:
            print(f"File {table_path} not found. Skipping...")
            r2_values.append(None)
        except IndexError:
            print(f"Error extracting R2 value from {table_path}. Skipping...")
            r2_values.append(None)

    # 将当前 unit 的 R2 值添加到合并的 DataFrame 中
    new_row = pd.Series(r2_values, index=merged_df.columns)
    merged_df = pd.concat([merged_df, new_row.to_frame().T], ignore_index=True)

# 保存合并后的表格
merged_df.to_excel(merge_save_path, index=False)
    