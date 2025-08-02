import pandas as pd
import os

# 读取包含模型名称的 Excel 文件
df_models = pd.read_excel("download_tools/baseline.xlsx")
models = list(df_models['models'])
# 提取实际的模型名称
models = [model.split('/')[-1] for model in models]
merge_save_path = "analysis/tools/hyperparameter_experiments/2_normalize/normalize_merge_tables.xlsx"

# 定义要处理的 normalize_threshold 范围
normalize_thresholds = [-25, -30, -35, -40, -45, -50]
normalize_threshold_columns = [f"[{t}, 0]" for t in normalize_thresholds]

# 初始化一个空的 DataFrame 用于存储合并后的数据，第一列是 normalize_threshold
merged_df = pd.DataFrame(columns=['Pre-normalization range'] + models)

# 遍历每个 normalize_threshold
for i, normalize_threshold in enumerate(normalize_thresholds):
    r2_values = [normalize_threshold_columns[i]]
    # 遍历每个模型
    for model in models:
        table_path = f"analysis/tools/hyperparameter_experiments/2_normalize/tables/{model}_{normalize_threshold}.xlsx"
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

    # 将当前 normalize_threshold 的 R2 值添加到合并的 DataFrame 中
    new_row = pd.Series(r2_values, index=merged_df.columns)
    merged_df = pd.concat([merged_df, new_row.to_frame().T], ignore_index=True)

# 保存合并后的表格
merged_df.to_excel(merge_save_path, index=False)
    