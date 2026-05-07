<h2 align="center">Beyond Scaling：测量与预测语言模型预训练中的知识保留上界</h2>

<p align="center">
  <a href="https://arxiv.org/abs/2502.04066"><img src="https://img.shields.io/badge/论文-Arxiv-blue.svg?style=for-the-badge" alt="论文"></a>
  <a href="https://aclanthology.org/"><img src="https://img.shields.io/badge/会议-ACL%202026-orange.svg?style=for-the-badge" alt="ACL 2026"></a>
  <a href="https://huggingface.co/EleutherAI/pythia-12b"><img src="https://img.shields.io/badge/模型-Pythia-yellow.svg?style=for-the-badge" alt="Pythia"></a>
</p>

> **注意：** 英文版 README 请参阅 [README.md](README.md)。

<p align="center">
  <img src="./assets/images/intro.jpg" alt="Beyond Scaling — 整体框架" width="85%">
</p>

## 🔔 最新消息

- 🏆 **[2026-04]** 论文被 **ACL 2026 主会** 录用。
- 🎉 **[2025-02]** 论文发布于 arXiv：[arXiv:2502.04066](https://arxiv.org/abs/2502.04066)。

## 📚 项目简介

一个语言模型究竟能从预训练语料中**保留**多少事实知识？这一上界是否能在**训练之前**就被预测出来？本工作系统研究了**预训练语料中的共现统计**（主语–宾语共现频率）与**下游事实回忆能力**之间的关系，并提出一种度量方式，能够预测知识保留的**上界**——揭示了纯粹的 Scaling Law 背后被忽视的因素。

我们以 **Pythia** 模型族与三个大规模预训练语料——**The Pile**、**ROOTS**、**SlimPajama**——为分析对象，并基于 **ParaRel** 风格的 15 个关系类构建带改写模板的事实探针。

### ✨ 核心亮点

- 🔍 **语料端测量** — 在 The Pile / ROOTS / SlimPajama 上对主语–宾语共现频率进行高效搜索
- 🧪 **模型端探针** — 在 **Pythia** 全系列模型上对 15 类关系进行带改写模板的知识探针
- 📈 **预测性分析** — 定量刻画预训练共现频率与事实回忆**上界**之间的关系，超越 Scaling Law 趋势
- 🛠️ **端到端流水线** — 语料下载 · 频率搜索 · vLLM/Transformers 推理 · 图表复现

## 📂 项目结构

```
SMI/
├── assets/                       # 🖼️ 论文配图（intro.jpg 等）
├── download_tools/               # ⬇️ 预训练语料 & 模型下载脚本
│   ├── pile/                     #     The Pile 下载
│   ├── roots/                    #     ROOTS 下载
│   ├── download_huggingface_model.py
│   └── baseline.xlsx
├── search/                       # 🔍 共现频率搜索
│   ├── pararel_15classes.json    #     ParaRel 风格探针集（15 类关系）
│   ├── pile/                     #     在 The Pile 上搜索
│   ├── roots/                    #     在 ROOTS 上搜索
│   ├── slimpajama/               #     在 SlimPajama 上搜索
│   ├── ours/                     #     我们整理 / 合并后的搜索结果
│   └── tools/                    #     搜索工具
├── infer/                        # 🤖 模型推理 / 探针
│   ├── infer_vllm.py             #     基于 vLLM 的高吞吐推理
│   ├── infer_transformers.py     #     HuggingFace Transformers 推理
│   ├── multi_templates.json      #     每种关系的多模板改写
│   ├── infer.sh                  #     批量推理启动脚本
│   ├── install.sh                #     环境安装
│   └── merge_outputs/            #     推理输出合并
├── analysis/                     # 📊 结果分析
│   ├── main_figures/             #     主图代码
│   ├── main_tables/              #     主表代码
│   ├── tables/                   #     辅助表格
│   └── tools/                    #     分析工具
├── pictures/                     # 🎨 图表生成脚本（matplotlib）
│   ├── cooccur_frequency.py / .pdf
│   ├── pythia_acc.py / .pdf
│   ├── eval_data.py / .pdf
│   └── colors.py
└── tables/                       # 📑 数据 / 评测元信息
    ├── data_info.py
    └── data_info{,_raw}.xlsx
```

## 🛠️ 使用指南

### 1. 环境配置

```bash
cd infer
bash install.sh
```

此脚本会安装 `vllm`、`transformers` 等推理依赖。

### 2. 下载预训练语料与模型

The Pile / ROOTS 的下载工具位于 `download_tools/`：

```bash
# 下载 The Pile 分片
cd download_tools/pile && bash <download_script>

# 从 Hugging Face 下载 Pythia 检查点
python download_tools/download_huggingface_model.py \
    --repo EleutherAI/pythia-12b \
    --out  /path/to/models/pythia-12b
```

> ⚠️ 两个语料都达到 TB 级，请提前预留好磁盘和带宽。

### 3. 共现频率搜索

我们统计探针集中每一组 `(主语, 宾语)` 在各预训练语料中的共现频率。在对应的 `search/` 子目录下运行搜索流水线：

```bash
# Pile / ROOTS / SlimPajama 各自有独立流水线
cd search/pile       && bash <search_script>
cd search/roots      && bash <search_script>
cd search/slimpajama && bash <search_script>
```

合并后的结果统一存放在 `search/ours/`，供下游分析使用。

### 4. 模型探针（vLLM / Transformers）

```bash
# 推荐：vLLM 高吞吐探针
python infer/infer_vllm.py \
    --model /path/to/pythia-XX \
    --prompts infer/multi_templates.json \
    --probe   search/pararel_15classes.json \
    --out     infer/merge_outputs/pythia-XX.jsonl

# 或使用 HuggingFace Transformers
python infer/infer_transformers.py --model /path/to/pythia-XX ...
```

每个事实都会用 `multi_templates.json` 中的**多个改写模板**询问模型，以降低模板敏感性。批量启动详见 `infer/infer.sh`。

### 5. 复现图表

完成推理输出与语料搜索之后：

```bash
# 主图（如 Scaling vs. 知识保留上界）
python analysis/main_figures/<figure_name>.py

# 主表
python analysis/main_tables/<table_name>.py

# 单独的 matplotlib 图（Pythia 准确率、共现频率等）
python pictures/pythia_acc.py
python pictures/cooccur_frequency.py
python pictures/eval_data.py
```

## 📝 引用

如果本项目对您的研究有帮助，欢迎引用：

```bibtex
@inproceedings{jiang-zhang-2026-beyondscaling,
    title     = "Beyond Scaling: Measuring and Predicting the Upper Bound of Knowledge Retention in Language Model Pre-Training",
    author    = "Jiang, Changhao and Zhang, Ming and Cao, Yifei and Ye, Junjie and
                 Fan, Xiaoran and Dou, Shihan and Xi, Zhiheng and Sun, Jiajun and
                 Dong, Yi and Shen, Yujiong and Tong, Jingqi and Fan, Baoyu and
                 Gui, Tao and Zhang, Qi and Huang, Xuanjing",
    booktitle = "Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics",
    year      = "2026",
    publisher = "Association for Computational Linguistics",
    url       = "https://arxiv.org/abs/2502.04066"
}
```

## 🔗 相关项目

| 项目 | 说明 | 链接 |
|------|------|------|
| **Pythia** | 探针实验所用的开源大模型族 | [GitHub](https://github.com/EleutherAI/pythia) |
| **ParaRel** | 改写式关系探针数据集 | [GitHub](https://github.com/yanaiela/pararel) |
| **LLMEval-Fair**（ACL 2026） | 鲁棒公平的大模型评测 | [GitHub](https://github.com/llmeval/LLMEval-Fair) |

## 📞 联系我们

如有问题或合作意向，请：

- 在 GitHub 上提交 [Issue](https://github.com/yuhui1038/SMI/issues)
- 联系项目维护者：
  - **姜昌昊（Changhao Jiang）**：chjiang24@m.fudan.edu.cn
  - **张明（Ming Zhang）**：mingzhang23@m.fudan.edu.cn

---

<p align="center">
  <b>Beyond Scaling</b> | 复旦大学自然语言处理实验室
</p>
