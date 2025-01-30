import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import json
import math
from scipy import stats
import os
import copy
import warnings
import matplotlib.font_manager as fm
import matplotlib as mpl


warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='1.6')
args = parser.parse_args()
P = float(args.model)
model = f"{args.model}B"

def normalize_list(lst):
    x_min = min(lst)
    x_max = max(lst)
    normalized_lst = [(x - x_min) / (x_max - x_min) for x in lst]
    return normalized_lst

# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # 修改为你的字体路径
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

times_new_roman_large = fm.FontProperties(fname=font_path, size=30)  # 设置大字体

classes = ['plays', 'occupation', 'work', 'is-located', 'locate', 'found', 'born', 'die', 'air', 'headquarter', 'capital', 'citizen', 'create', 'play', 'is-locate', 'total']

for mod in ['co-occurence', 'MI', 'SMI']:
    if mod == 'co-occurrence':
        mode = 'cooccur'
    else:
        mode = 'mi'
    df_total = []
    results = pd.DataFrame(np.zeros([len(classes), 6]), columns=['cl', 'a', 'b', 'F', 'R2', 'MSE'])
    for c in range(len(classes)):
        cl = classes[c]
        data = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/analysis/correlation/{model}/{mode}/{cl}.xlsx'
        save_path = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/analysis/correlation/box_plot/picture_classes/{model}/{mod}/{model}_{mod}.jpg'
        figure_save_path = f'/mnt/data/user/xxx/projects/pt_mem/wikipedia/analysis/correlation/box_plot/picture_classes/figures/{model}_{mod}.pdf'
        os.makedirs('/'.join(save_path.split('/')[:-1]), exist_ok=True)
        os.makedirs('/'.join(figure_save_path.split('/')[:-1]), exist_ok=True)

        if cl == 'total':
            df = df_total
        else:
            df = pd.read_excel(data, index_col=0)
            df = df[df['rel_text'] == cl]
            df_total = df if len(df_total) == 0 else pd.concat([df_total, df])

        df = df.reset_index(drop=True)

        # 
        metric = list(df['metric'])
        metric = normalize_list(metric)
        if mod == 'SMI':
            for i in range(len(df)):
                metric[i] = metric[i] ** (1 + 1 / P)
        df['metric'] = metric

        sums = dict()
        mis = dict()
        variances = dict()

        metric = df['metric']
        corrects = df['correct']

        for i in range(len(df)):
            variances[metric[i]] = variances[metric[i]] + [corrects[i]] if variances.get(metric[i]) else [corrects[i]]
            mis[metric[i]] = mis[metric[i]] + corrects[i] if mis.get(metric[i]) else corrects[i]
            sums[metric[i]] = sums[metric[i]] + 1 if sums.get(metric[i]) else 1

        for key in mis.keys():
            mis[key] /= sums[key]

        slope, intercept, r_value, p_value, std_err = stats.linregress(list(mis.keys()), list(mis.values()))
        r_value = r_value ** 2
        for key in variances.keys():
            mean = slope * key + intercept
            n = len(variances[key])
            squared_diffs = [(val - mean) ** 2 for val in variances[key]]
            variance = sum(squared_diffs) / n
            std_dev = math.sqrt(variance)
            variances[key] = variance
        variances = dict(sorted(variances.items(), key=lambda item: item[0]))

        results['cl'][c] = cl
        results['a'][c] = slope
        results['b'][c] = intercept
        results['R2'][c] = r_value
        results['MSE'][c] = sum(list(variances.values())) / len(list(variances.values()))
        if intercept >= 0:
            results['F'][c] = f'y = {slope:.3f}x + {intercept:.3f}'
        else:
            results['F'][c] = f'y = {slope:.3f}x - {-intercept:.3f}'

        if cl == 'total':
            df2 = pd.DataFrame(np.zeros([len(mis), 3]), columns=[f'{mod}', 'ACC', 'Count'])
            df2[f'{mod}'] = list(mis.keys())
            df2['ACC'] = list(mis.values())
            df2['Count'] = list(sums.values())
            df2 = df2.sort_values(by=f'{mod}')
            df2 = df2.reset_index(drop=True)
            df2.to_excel(f"{'/'.join(save_path.split('/')[:-1])}/sum.xlsx")
            df.to_excel(f"{'/'.join(save_path.split('/')[:-1])}/total.xlsx")


        plt.figure(figsize=(8, 8))
        ax = plt.subplot()
        ax.scatter(mis.keys(), mis.values(), alpha=1, edgecolors='black', linewidths=0.8, s=50, c=mis.values(), cmap='viridis', label='Average ACC')

        ax.plot((0, 1), [intercept, slope + intercept], color=(0.898, 0.553, 0.733), label='Predicted', linewidth=5)

        fontsize = 20
        plt.xlabel(f'{mod}', fontproperties=times_new_roman_large)

        plt.xlim(0, 1)
        plt.ylim(0, 1)

        plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontproperties=times_new_roman_large)
        plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontproperties=times_new_roman_large)
        plt.ylabel('ACC', fontproperties=times_new_roman_large)

        ax.legend(loc='upper left', fontsize=fontsize, prop=times_new_roman_large)

        r2 = round(r_value, 3)
        mse = round(results['MSE'][c], 3)
        ax.text(0.4, 0.5, f"R² = {r2}\nMSE = {mse}", fontproperties=times_new_roman_large, ha='right')

        if cl == 'total':
            plt.savefig(save_path, dpi=600, bbox_inches='tight')
            plt.savefig(figure_save_path, dpi=600, bbox_inches='tight')
            results.to_excel(f"{'/'.join(save_path.split('/')[:-1])}/results.xlsx")
            print(len(mis), model, mod)
