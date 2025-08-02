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
import multiprocessing
import traceback

# warnings.filterwarnings('ignore')
# 检查字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/times.ttf'  # 修改为你的字体路径
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")
times_new_roman_large = fm.FontProperties(fname=font_path, size=30)  # 设置大字体

normalize_threshold = -30

def normalize_list(lst, method):
    for i in range(len(lst)):
        lst[i] = int(math.log2(lst[i]) * 5) / 5
    x_min = min(lst)
    x_max = max(lst)
    if 'MI' in method:
        x_min = normalize_threshold
        x_max = 0
        # for x in lst:
        #     if x > 0 or x < -30:
        #         print(x, '____________')
    # print(x_min, x_max)
    normalized_lst = [(x - x_min) / (x_max - x_min) for x in lst]
    return normalized_lst


def analysis_data(model, P, unit):
    P = P * 1e9
    data_path = f"infer/merge_outputs/{model}.json"
    with open(data_path, 'r') as f:
        data = json.load(f)
        data = [js for js in data if js['mi'] >= 2 ** normalize_threshold]
    corrects = [js['acc'] for js in data]

    results = pd.DataFrame(np.zeros([1, 7]), columns=['model', 'method', 'a', 'b', 'F', 'R2', 'MSE'])
    method = 'SMI'
    excel_save_path = f"analysis/tools/hyperparameter_experiments/1_unit/tables/{model}_{unit}.xlsx"
    figure_save_path = f"analysis/tools/hyperparameter_experiments/1_unit/figures/{model}_{unit}.pdf"

    mode = 'mi'
    metrics = [js[mode] for js in data]
    metrics = normalize_list(metrics, method)

    for i in range(len(metrics)):
        metrics[i] = metrics[i] ** (1 + 1 / (P / unit))

    sums = dict()
    mis = dict()
    variances = dict()
    for i in range(len(metrics)):
        variances[metrics[i]] = variances[metrics[i]] + [corrects[i]] if variances.get(metrics[i]) else [corrects[i]]
        mis[metrics[i]] = mis[metrics[i]] + corrects[i] if mis.get(metrics[i]) else corrects[i]
        sums[metrics[i]] = sums[metrics[i]] + 1 if sums.get(metrics[i]) else 1
    for key in mis.keys():
        mis[key] /= sums[key]

    slope, intercept, r_value, p_value, std_err = stats.linregress(list(mis.keys()), list(mis.values()))
    r2 = r_value ** 2
    for key in variances.keys():
        mean = slope * key + intercept
        n = len(variances[key])
        squared_diffs = [(val - mean) ** 2 for val in variances[key]]
        variance = sum(squared_diffs) / n
        std_dev = math.sqrt(variance)
        variances[key] = variance
    variances = dict(sorted(variances.items(), key=lambda item: item[0]))

    results.loc[0, 'model'] = model
    results.loc[0, 'method'] = method
    results.loc[0, 'a'] = slope
    results.loc[0, 'b'] = intercept
    results.loc[0, 'R2'] = r2
    mse = sum(list(variances.values())) / len(list(variances.values()))
    results.loc[0, 'MSE'] = mse
    if intercept >= 0:
        results.loc[0, 'F'] = f'y = {slope:.3f}x + {intercept:.3f}'
    else:
        results.loc[0, 'F'] = f'y = {slope:.3f}x - {-intercept:.3f}'

    plt.figure(figsize=(8, 8))
    ax = plt.subplot()
    ax.scatter(mis.keys(), mis.values(), alpha=1, edgecolors='black', linewidths=0.8, s=50, c=list(mis.values()), cmap='viridis', label='Average ACC')
    ax.plot((0, 1), [intercept, slope + intercept], color=(0.898, 0.553, 0.733), label='Predicted', linewidth=5)

    plt.xlabel(f'{method}', fontproperties=times_new_roman_large)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontproperties=times_new_roman_large)
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontproperties=times_new_roman_large)
    plt.ylabel('ACC', fontproperties=times_new_roman_large)
    ax.legend(loc='upper left', prop=times_new_roman_large)

    r2 = round(r2, 3)
    mse = round(mse, 3)
    ax.text(0.4, 0.5, f"R² = {r2}\nMSE = {mse}", fontproperties=times_new_roman_large, ha='right')

    plt.savefig(figure_save_path, dpi=600, bbox_inches='tight')
    results.to_excel(excel_save_path)
    print(len(mis), model, method)


if __name__ == "__main__":
    if not os.path.exists("analysis/tools/hyperparameter_experiments/1_unit/figures"):
        os.mkdir("analysis/tools/hyperparameter_experiments/1_unit/figures")
    if not os.path.exists("analysis/tools/hyperparameter_experiments/1_unit/tables"):
        os.mkdir("analysis/tools/hyperparameter_experiments/1_unit/tables")
    df = pd.read_excel("download_tools/baseline.xlsx")
    # 创建一个进程池，默认使用CPU核心数
    pool = multiprocessing.Pool()
    results = []
    units = [10 ** i for i in range(21)]  # 生成 10e7 到 10e11 的 unit 列表
    for unit in units:
        for i in range(len(df)):
            model = df.loc[i, 'models'].split('/')[-1]
            P = df.loc[i, 'model_size']
            # 异步执行analysis_data函数
            result = pool.apply_async(analysis_data, args=(model, P, unit))
            results.append(result)
    # 关闭进程池，不再接受新的任务
    pool.close()
    # 等待所有进程完成任务
    pool.join()
    # 获取每个进程的结果（如果analysis_data函数有返回值）
    for result in results:
        try:
            result.get()
        except Exception as e:
            print(f"An error occurred: {e}")
            # traceback.print_exc()