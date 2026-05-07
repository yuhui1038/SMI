<h2 align="center">Beyond Scaling：测量与预测语言模型预训练中的知识保留上界</h2>

<p align="center">
  <a href="https://arxiv.org/abs/2502.04066"><img src="https://img.shields.io/badge/论文-Arxiv-blue.svg?style=for-the-badge" alt="论文"></a>
  <a href="https://arxiv.org/pdf/2502.04066"><img src="https://img.shields.io/badge/PDF-arXiv-red.svg?style=for-the-badge" alt="PDF"></a>
  <img src="https://img.shields.io/badge/会议-ACL%202026%20Main-orange.svg?style=for-the-badge" alt="ACL 2026 Main">
</p>

> **注意：** 英文版 README 请参阅 [README.md](README.md)。

<p align="center">
  <img src="./assets/images/intro.jpg" alt="Beyond Scaling — 整体框架" width="85%">
</p>

## 🔔 最新消息

- 🏆 **[2026-04]** 论文被 **ACL 2026 主会** 录用。
- 🎉 **[2025-02]** 论文发布于 arXiv：[arXiv:2502.04066](https://arxiv.org/abs/2502.04066)。

## 📚 项目简介

一个语言模型究竟能从预训练语料中**保留**多少事实知识？这一上界是否能在**训练之前**就被预测出来？本工作直接对**知识保留**——模型记住语料中事实信息的能力——进行建模，并提出一种**在训练前就能估计**该能力的原则化方法。

我们提出 **SMI**（**Size-dependent Mutual Information**，规模依赖的互信息），一种信息论预测指标，融合**知识频率**、**知识独特性**与**模型规模**三方面信息，用于预测**闭卷问答（Closed-book QA）**的准确率。SMI 通过对 **21 个公开模型** + **3 个自训模型**所披露的预训练语料进行大规模文档检索来验证，并辅以鲁棒的多模板 QA 评测。实验表明：SMI 显著优于基于重复频次的基线，对参数量大于 1B 的模型在闭卷问答上可达到 **R² > 0.7** 的预测精度——**完全无需额外训练**。分析还揭示了数据与模型规模扩展的边际效益递减，并给出了仅靠预训练所能达到的**知识保留内在上界**的量化证据。

### ✨ 核心亮点

- 📐 **SMI 指标** — 信息论预测指标，整合**知识频率**、**知识独特性**和**模型规模**
- 🔍 **语料端测量** — 在 **The Pile**、**ROOTS**、**SlimPajama** 等已披露的预训练语料上进行大规模文档检索
- 🧪 **模型端评测** — 跨 **21 个公开模型** + **3 个自训模型**的鲁棒多模板 QA 评测
- 📈 **强预测能力** — 在 1B 以上模型上闭卷 QA 准确率预测 **R² > 0.7**，显著优于重复频次基线
- 🪜 **超越 Scaling** — 量化证据表明仅靠预训练存在**内在的知识保留上界**
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

探针流水线支持任意 HuggingFace 兼容的 Causal LM。论文中我们将其应用于 **21 个公开模型**（如 Pythia、BLOOM、TinyLlama 等）以及 **3 个自训模型**：

```bash
# 推荐：vLLM 高吞吐探针
python infer/infer_vllm.py \
    --model /path/to/<model_dir> \
    --prompts infer/multi_templates.json \
    --probe   search/pararel_15classes.json \
    --out     infer/merge_outputs/<model_name>.jsonl

# 或使用 HuggingFace Transformers
python infer/infer_transformers.py --model /path/to/<model_dir> ...
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
@misc{jiang2025beyondscaling,
      title         = {Beyond Scaling: Measuring and Predicting the Upper Bound of
                       Knowledge Retention in Language Model Pre-Training},
      author        = {Changhao Jiang and Ming Zhang and Yifei Cao and Junjie Ye and
                       Xiaoran Fan and Shihan Dou and Zhiheng Xi and Jiajun Sun and
                       Yi Dong and Yujiong Shen and Jingqi Tong and Baoyu Fan and
                       Tao Gui and Qi Zhang and Xuanjing Huang},
      year          = {2025},
      eprint        = {2502.04066},
      archivePrefix = {arXiv},
      primaryClass  = {cs.CL},
      url           = {https://arxiv.org/abs/2502.04066},
      note          = {Accepted at ACL 2026 (Main)}
}
```

> ACL 2026 会议论文集发布后，将以官方 ACL Anthology 的 BibTeX 替换此处。

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
