import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from colors import colors5, colors15, colors5_light
import matplotlib.font_manager as fm
import os

save_path = 'pictures/main_R2_small.pdf'

# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # 修改为你的字体路径
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

times_new_roman = fm.FontProperties(fname=font_path, size=24)  # 设置字体和大小
times_new_roman2 = fm.FontProperties(fname=font_path, size=20)  # 设置字体和大小

# Data
models = ['bloom-560m', 'gpt-neo-1.3B', 'pythia-14m', 'ours-1.6b']
models_name = ['bloom-560m', 'gpt-neo-1.3B', 'pythia-14m', 'ours-1.6b']
cooccur_metric = []
MI_metric = []
SMI_metric = []

r2_table = pd.read_excel("analysis/main_tables/r2_table.xlsx")

for model in models:
    for i in range(len(r2_table)):
        if r2_table.loc[i, 'model'] == model:
            cooccur_metric.append(r2_table.loc[i, 'CO-OCCUR'])
            MI_metric.append(r2_table.loc[i, 'MI'])
            SMI_metric.append(r2_table.loc[i, 'SMI'])

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.2
index = range(len(models))

colors = colors15[-3:]

bar1 = plt.bar([i - bar_width for i in index], cooccur_metric, bar_width, label='CO-OCCUR', color=colors[0], edgecolor='black', linewidth=0.5)
bar2 = plt.bar(index, MI_metric, bar_width, label='MI', color=colors[1], edgecolor='black', linewidth=0.5)
bar3 = plt.bar([i + bar_width for i in index], SMI_metric, bar_width, label='SMI', color=colors[2], edgecolor='black', linewidth=0.5)

ax.grid(axis='both', linestyle='--', color='gray', alpha=0.5)

plt.ylim(0.2, 1)
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], fontproperties=times_new_roman)

# plt.xlabel('Models', fontproperties=times_new_roman)
plt.ylabel('R²', fontproperties=times_new_roman)
plt.xticks(index, models_name, fontproperties=times_new_roman)
plt.legend(loc='upper left', prop=times_new_roman2)

plt.tight_layout()

# 显示图形
plt.savefig(save_path, dpi=600, bbox_inches='tight')
plt.show()
