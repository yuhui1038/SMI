import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os
from colors import colors5, colors15, colors5_light
import matplotlib as mpl
import json


def generate_gradient_normalized(color1, color2, steps):
    """
    生成两个归一化RGB颜色之间的线性渐变色。
    
    :param color1: 起始颜色，(R, G, B)，每个值在 [0, 1] 范围内
    :param color2: 结束颜色，(R, G, B)，每个值在 [0, 1] 范围内
    :param steps: 渐变的步数，包括起始和结束颜色
    :return: 渐变颜色的列表，包含 `steps` 个颜色
    """
    gradient = []
    for i in range(steps):
        t = i / (steps - 1)  # 插值因子，范围从 0 到 1
        new_color = (
            color1[0] + t * (color2[0] - color1[0]),
            color1[1] + t * (color2[1] - color1[1]),
            color1[2] + t * (color2[2] - color1[2]),
        )
        gradient.append(new_color)
    return gradient

save_path = "pictures/cooccur_frequency.pdf"

# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # Modify this path as needed
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

times_new_roman = fm.FontProperties(fname=font_path, size=24)

# Read the data
with open("search/pile/merge.json", 'r') as f:
    data = json.load(f)
cooccurs = [js['time_s1j1'] for js in data if js['time_s1j1']>0]

# Generate x-axis values by taking the logarithm base 10 of the cooccurs list
x_values = np.log2(cooccurs)

# Create bins
bins = np.arange(int(x_values.min()), int(x_values.max()) + 2)

# Use np.histogram to calculate the frequency of each bin
hist, bin_edges = np.histogram(x_values, bins=bins)

# colors = generate_gradient_normalized(colors5_light[5], colors5[5], len(bin_edges)-1)
colors = [colors5_light[5]] * 15

# Plot the bar chart
fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(bin_edges[:-1], hist, width=1, align='edge', color=colors, edgecolor='black', linewidth=0.2, label='Co-occurrence Frequencies')  # Add black border

# Labeling the axes with custom font
ax.set_xlabel('Co-occurrence Frequencies', fontproperties=times_new_roman)
ax.set_ylabel('Frequency', fontproperties=times_new_roman)
# ax.set_title('Frequency Histogram of Co-occurrences', fontproperties=times_new_roman)

# 在特定列添加竖线
specific_columns = [0, 5, 10, 15, 20]
for col in specific_columns:
    ax.axvline(x=col, linestyle='--', color='gray', alpha=0.5)

# 添加横线网格
ax.grid(axis='y', linestyle='--', color='gray', alpha=0.5)

# Set x-ticks and labels
ax.set_xticks(bins)
# ax.set_xticklabels([f'$8^{{{b//3}}}$' if b % 3 == 0 else '' for b in bins], fontproperties=times_new_roman)
# ax.set_xticklabels([f'$2^{{{b}}}$' if b % 4 == 0 else '' for b in bins], fontproperties=times_new_roman)
ax.set_xticklabels([f'$2^{{{b}}}$' if b % 5 == 0 else '' for b in bins], fontproperties=times_new_roman)

plt.yticks([0, 500, 1000, 1500, 2000, 2500], fontproperties=times_new_roman)
# plt.yticks([0, 1000, 2000, 3000, 4000, 5000], fontproperties=times_new_roman)

# Apply custom font to the legend
# plt.legend(prop=times_new_roman)

# Display
plt.tight_layout()
plt.savefig(save_path, dpi=600, bbox_inches='tight')
plt.show()
