import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from colors import colors5, colors15, colors5_light
import matplotlib.font_manager as fm
import os

save_path = 'pictures/main_MSE.pdf'

# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # 修改为你的字体路径
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

times_new_roman = fm.FontProperties(fname=font_path, size=20)  # 设置字体和大小

# Data
models = ['bloom', 'gpt-neox-20b', 'pythia-12b', 'TinyLlama-1.1B-intermediate-step-480k-1T', 'ours-13b']
models_name = ['bloom (176b)', 'gpt-neox-20b', 'pythia-12b', 'TinyLlama-1.1B', 'ours-13b']
cooccur_metric = []
MI_metric = []
SMI_metric = []

mse_table = pd.read_excel("analysis/main_tables/mse_table.xlsx")

for model in models:
    for i in range(len(mse_table)):
        if mse_table.loc[i, 'model'] == model:
            cooccur_metric.append(mse_table.loc[i, 'CO-OCCUR'])
            MI_metric.append(mse_table.loc[i, 'MI'])
            SMI_metric.append(mse_table.loc[i, 'SMI'])

# Plot
fig, ax = plt.subplots(figsize=(10, 8))

bar_width = 0.2
index = range(len(models))

colors = colors15[-3:]

bar1 = plt.bar([i - bar_width for i in index], cooccur_metric, bar_width, label='CO-OCCUR', color=colors[0], edgecolor='black')
bar2 = plt.bar(index, MI_metric, bar_width, label='MI', color=colors[1], edgecolor='black')
bar3 = plt.bar([i + bar_width for i in index], SMI_metric, bar_width, label='SMI', color=colors[2], edgecolor='black')

plt.ylim(0.06, 0.1)
plt.yticks([0.06, 0.07, 0.08, 0.09, 0.1], fontproperties=times_new_roman)

plt.xlabel('Models', fontproperties=times_new_roman)
plt.ylabel('MSE', fontproperties=times_new_roman)
plt.xticks(index, models_name, fontproperties=times_new_roman)
plt.legend(loc='upper right', prop=times_new_roman)

plt.tight_layout()

# 显示图形
plt.savefig(save_path, dpi=600, bbox_inches='tight')
plt.show()
