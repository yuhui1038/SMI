import pandas as pd

# 读取包含模型名称的 Excel 文件
df_models = pd.read_excel("download_tools/baseline.xlsx")
models = list(df_models['models'])
save_path = "analysis/main_tables/main_table.xlsx"
r2_save_path = "analysis/main_tables/r2_table.xlsx"
mse_save_path = "analysis/main_tables/mse_table.xlsx"

for i, model in enumerate(models):
    model = model.split('/')[-1]
    df_path = f"analysis/tables/{model}.xlsx"
    # 读取当前模型对应的 Excel 文件
    try:
        current_df = pd.read_excel(df_path, index_col=0)
    except:
        continue
    if i == 0:
        output_df = current_df
    else:
        # 合并 DataFrame
        output_df = pd.concat([output_df, current_df], ignore_index=True)

# output_df = output_df.drop(['a', 'b', 'F'], axis=1)
# 将合并后的 DataFrame 保存为 Excel 文件
output_df.to_excel(save_path, index=False)


# 只保留需要的列
r2_df = output_df[['model', 'method', 'R2']]
# 记录 model 列的原始顺序
original_model_order = r2_df['model'].unique()
# 使用 pivot 方法重新组织数据
r2_df = r2_df.pivot(index='model', columns='method', values='R2')
# 按照原始顺序重新排序
r2_df = r2_df.reindex(original_model_order)
# 重置索引
r2_df = r2_df.reset_index()
# 将结果保存为 Excel 文件
r2_df.to_excel(r2_save_path, index=False)


# 只保留需要的列
mse_df = output_df[['model', 'method', 'MSE']]
# 记录 model 列的原始顺序
original_model_order = mse_df['model'].unique()
# 使用 pivot 方法重新组织数据
mse_df = mse_df.pivot(index='model', columns='method', values='MSE')
# 按照原始顺序重新排序
mse_df = mse_df.reindex(original_model_order)
# 重置索引
mse_df = mse_df.reset_index()
# 将结果保存为 Excel 文件
mse_df.to_excel(mse_save_path, index=False)