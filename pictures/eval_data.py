import matplotlib.pyplot as plt
import pandas as pd
from colors import colors5, colors15, colors5_light
import matplotlib.font_manager as fm
import os
import numpy as np
from matplotlib.patches import ConnectionPatch


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

save_path = 'pictures/eval_data.pdf'

# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # 根据需要修改此路径
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

times_new_roman = fm.FontProperties(fname=font_path, size=24)

# 数据
relations = [
    "work", "capital", "locate", "headquarter", "born", "air",
    "die", "occupation", "plays", "found", "is-located",
    "create", "is-locate", "citizen", "play"
]

amounts = []
data = pd.read_excel("tables/data_info.xlsx")
for relation in relations:
    for i in range(len(data)):
        if data.loc[i, 'relation'] == relation:
            amounts.append(data.loc[i, 'amounts'])
            break
print(f"amounts of eval data: {sum(amounts)}")

# 对数据进行排序
sorted_data = sorted(zip(amounts, relations))
amounts_sorted, relations_sorted = zip(*sorted_data)

# colors = generate_gradient_normalized(colors5_light[5], colors5[5], 15)
colors = [colors5_light[5]] * 15

# 绘制饼图
fig, ax = plt.subplots(figsize=(10, 8))
wedges1, texts1, autotexts1 = ax.pie(
    amounts_sorted,
    labels=None,
    startangle=90,
    colors=colors,
    autopct=lambda pct: '{:.0f}'.format(pct * sum(amounts_sorted) / 100.0),
    wedgeprops={"edgecolor": "white", "width": 1, "linewidth": 2},
    pctdistance=1.25
)
ax.axis('equal')  # 保持饼图为圆形

# 自定义内圈标签
for i, txt in enumerate(autotexts1):
    txt.set_text(f'{relations_sorted[i]}, {amounts_sorted[i]}')
    txt.set_fontproperties(times_new_roman)
    if 'work' in txt.get_text():
        txt.set_position([-0.15, 1.3])
    if 'headquarter' in txt.get_text():
        txt.set_position([-1.4, 0.15])
    if 'is-located' in txt.get_text():
        txt.set_position([1.3, -0.45])
    if 'occupation' in txt.get_text():
        txt.set_position([0, -1.35])
    if 'citizen' in txt.get_text():
        txt.set_position([1.3, 0.2])

# 在饼图和标签之间添加引导线
for i, (wedge, txt) in enumerate(zip(wedges1, autotexts1)):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x = wedge.r * 1.2 * np.cos(np.deg2rad(angle))
    y = wedge.r * 1.2 * np.sin(np.deg2rad(angle))
    connector = ConnectionPatch(
        xyA=(x * 0.7, y * 0.7), xyB=(x * 0.89, y * 0.89), coordsA='data', coordsB='data',
        axesA=ax, axesB=ax, color='black'
    )
    ax.add_artist(connector)
    # txt.set_position((x, y))

# 保存并显示
plt.tight_layout()
plt.savefig(save_path, dpi=600, bbox_inches='tight')
plt.show()
