import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.font_manager as fm
from colors import colors5, colors15, colors5_light


save_path = 'pictures/pythia_acc.pdf'

# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # 修改为你的字体路径
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

times_new_roman = fm.FontProperties(fname=font_path, size=24)  # 设置字体和大小

# 读取第一个文件
main_table = pd.read_excel('analysis/main_tables/main_table.xlsx')
# 读取第二个文件
baseline = pd.read_excel('download_tools/baseline.xlsx')

# 处理第二个文件的 models 列
baseline['model_name'] = baseline['models'].apply(lambda x: x.split('/')[-1])

# 去除 main_table 中的重复模型（保留第一个出现的值）
main_table_unique = main_table.drop_duplicates(subset='model', keep='first')

# 合并两个 DataFrame
merged = pd.merge(baseline, main_table_unique, left_on='model_name', right_on='model', how='left')

# 对 model_size 取 log2
merged['model_size_log2'] = np.log2(merged['model_size'])

# 按不同类别绘制折线
categories = ['bloom', 'gpt', 'pythia', 'TinyLlama', 'ours']
colors = ['r', 'g', 'b', 'y', 'c']
colors = colors5[:5]

fig, ax = plt.subplots(figsize=(10, 6))

for cat, color in zip(categories, colors):
    subset = merged[merged['model_name'].str.contains(cat)]
    ax.plot(subset['model_size_log2'], subset['acc'], marker='o', linestyle='-', color=color, label=cat)

# 添加标题和轴标签
# ax.set_title('Model Accuracy Comparison', fontproperties=times_new_roman)
ax.set_xlabel('Log2 of Model Size', fontproperties=times_new_roman)
ax.set_ylabel('Accuracy', fontproperties=times_new_roman)

plt.xticks([-8, -4, 0, 4, 8], fontproperties=times_new_roman)
plt.yticks([0.05, 0.1, 0.15, 0.2, 0.25], fontproperties=times_new_roman)

# 添加图例
ax.legend(prop=times_new_roman)

# 显示网格线
ax.grid(axis='both', linestyle='--', color='gray', alpha=0.5)

# 保存图形
plt.savefig(save_path, dpi=600, bbox_inches='tight')

# 显示图形
plt.show()