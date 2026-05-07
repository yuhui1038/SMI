<h2 align="center">Beyond Scaling: Measuring and Predicting the Upper Bound of Knowledge Retention in Language Model Pre-Training</h2>

<p align="center">
  <a href="https://arxiv.org/abs/2502.04066"><img src="https://img.shields.io/badge/Paper-Arxiv-blue.svg?style=for-the-badge" alt="Paper"></a>
  <a href="https://arxiv.org/pdf/2502.04066"><img src="https://img.shields.io/badge/PDF-arXiv-red.svg?style=for-the-badge" alt="PDF"></a>
  <img src="https://img.shields.io/badge/Venue-ACL%202026%20Main-orange.svg?style=for-the-badge" alt="ACL 2026 Main">
</p>

> **Note:** For the Chinese version of this README, please refer to [README_zh.md](README_zh.md).

<p align="center">
  <img src="./assets/images/intro.jpg" alt="Beyond Scaling — overview" width="85%">
</p>

## 🔔 News

- 🏆 **[2026-04]** Our paper has been accepted at **ACL 2026 Main**.
- 🎉 **[2025-02]** Our paper is released on arXiv: [arXiv:2502.04066](https://arxiv.org/abs/2502.04066).

## 📚 Overview

How much factual knowledge can a language model actually **retain** from its pre-training corpus, and is this upper bound predictable **before** training? This work models knowledge retention — a model's capacity to memorize factual information from its corpus — and introduces a principled method for estimating it *prior to training*.

We propose **SMI** (**Size-dependent Mutual Information**), an information-theoretic predictor that integrates **knowledge frequency**, **knowledge specificity**, and **model size** to forecast **closed-book QA** accuracy. SMI is validated through large-scale document retrieval over the disclosed pre-training corpora of **21 public** and **3 custom** models, combined with a robust multi-template QA evaluation. Experiments show that SMI significantly outperforms repetition-based baselines and achieves **R² > 0.7** on models above 1B parameters — *without any additional training*. The analysis further reveals diminishing returns from scaling data and model size, and provides evidence for an **intrinsic upper bound** on knowledge retention achievable by pre-training alone.

### ✨ Highlights

- 📐 **SMI metric** — an information-theoretic predictor combining *knowledge frequency*, *knowledge specificity* and *model size*
- 🔍 **Corpus-side measurement** — large-scale document retrieval over disclosed pre-training corpora (e.g. **The Pile**, **ROOTS**, **SlimPajama**)
- 🧪 **Model-side evaluation** — robust multi-template QA evaluation across **21 public** + **3 custom** models
- 📈 **Strong predictive power** — **R² > 0.7** on closed-book QA accuracy for models above 1B parameters, beating repetition-based baselines
- 🪜 **Beyond scaling** — quantitative evidence for an **intrinsic upper bound** on knowledge retention from pre-training alone
- 🛠️ **End-to-end pipeline** — corpus download · frequency search · vLLM/Transformers inference · figure & table reproduction

## 📂 Project Structure

```
SMI/
├── assets/                       # 🖼️ Paper figures (intro.jpg, etc.)
├── download_tools/               # ⬇️ Pre-training corpus & model downloaders
│   ├── pile/                     #     The Pile downloader
│   ├── roots/                    #     ROOTS downloader
│   ├── download_huggingface_model.py
│   └── baseline.xlsx
├── search/                       # 🔍 Co-occurrence frequency search
│   ├── pararel_15classes.json    #     ParaRel-style probe set (15 relation classes)
│   ├── pile/                     #     Search over The Pile
│   ├── roots/                    #     Search over ROOTS
│   ├── slimpajama/               #     Search over SlimPajama
│   ├── ours/                     #     Our merged / processed search results
│   └── tools/                    #     Search utilities
├── infer/                        # 🤖 Model probing / inference
│   ├── infer_vllm.py             #     vLLM-based fast inference
│   ├── infer_transformers.py     #     HuggingFace Transformers inference
│   ├── multi_templates.json      #     Paraphrased prompt templates per relation
│   ├── infer.sh                  #     Batch inference launcher
│   ├── install.sh                #     Environment setup
│   └── merge_outputs/            #     Inference output aggregation
├── analysis/                     # 📊 Result analysis
│   ├── main_figures/             #     Code for main paper figures
│   ├── main_tables/              #     Code for main paper tables
│   ├── tables/                   #     Auxiliary tables
│   └── tools/                    #     Analysis utilities
├── pictures/                     # 🎨 Figure-rendering scripts (matplotlib)
│   ├── cooccur_frequency.py / .pdf
│   ├── pythia_acc.py / .pdf
│   ├── eval_data.py / .pdf
│   └── colors.py
└── tables/                       # 📑 Dataset / evaluation metadata
    ├── data_info.py
    └── data_info{,_raw}.xlsx
```

## 🛠️ Usage Guide

### 1. Environment Setup

```bash
cd infer
bash install.sh
```

This installs `vllm`, `transformers`, and other inference dependencies.

### 2. Download Pre-training Corpora & Models

The Pile / ROOTS downloaders live under `download_tools/`:

```bash
# Example: download The Pile shards
cd download_tools/pile && bash <download_script>

# Example: download a Pythia checkpoint from Hugging Face
python download_tools/download_huggingface_model.py \
    --repo EleutherAI/pythia-12b \
    --out  /path/to/models/pythia-12b
```

> ⚠️ Both corpora are large (TB-scale). Make sure to allocate enough disk and bandwidth.

### 3. Co-occurrence Frequency Search

We measure how often each `(subject, object)` pair from the probe set co-occurs in each pre-training corpus. Run the corresponding searcher under `search/`:

```bash
# Pile / ROOTS / SlimPajama each have their own search pipeline
cd search/pile      && bash <search_script>
cd search/roots     && bash <search_script>
cd search/slimpajama && bash <search_script>
```

Results are merged under `search/ours/` for downstream analysis.

### 4. Model Probing (vLLM / Transformers)

The probing pipeline supports any HuggingFace-compatible causal LM. In the paper we use it on **21 public** (e.g. Pythia, BLOOM, TinyLlama, ...) and **3 custom** models:

```bash
# Recommended: vLLM for high-throughput probing
python infer/infer_vllm.py \
    --model /path/to/<model_dir> \
    --prompts infer/multi_templates.json \
    --probe   search/pararel_15classes.json \
    --out     infer/merge_outputs/<model_name>.jsonl

# Or use HuggingFace Transformers
python infer/infer_transformers.py --model /path/to/<model_dir> ...
```

Each fact is queried with **multiple paraphrased templates** (`multi_templates.json`) to reduce template sensitivity. See `infer/infer.sh` for batch launching.

### 5. Reproducing Figures & Tables

Once inference outputs and corpus-search results are available:

```bash
# Main figures (e.g., scaling vs. retention upper bound)
python analysis/main_figures/<figure_name>.py

# Main tables
python analysis/main_tables/<table_name>.py

# Standalone matplotlib figures (Pythia acc, co-occurrence freq, ...)
python pictures/pythia_acc.py
python pictures/cooccur_frequency.py
python pictures/eval_data.py
```

## 📝 Citation

If you find this work useful, please cite our paper:

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

> The official ACL Anthology BibTeX will replace this entry once the ACL 2026 proceedings are released.

## 🔗 Related Projects

| Project | Description | Link |
|---------|-------------|------|
| **Pythia** | Open-source LM suite used for our probing experiments | [GitHub](https://github.com/EleutherAI/pythia) |
| **ParaRel** | Paraphrased relation probing set | [GitHub](https://github.com/yanaiela/pararel) |
| **LLMEval-Fair** (ACL 2026) | Robust & fair evaluation of LLMs | [GitHub](https://github.com/llmeval/LLMEval-Fair) |

## 📞 Contact Us

For questions or collaboration, please:

- Open an [Issue](https://github.com/yuhui1038/SMI/issues) on GitHub
- Contact the project maintainers:
  - **Changhao Jiang**: chjiang24@m.fudan.edu.cn
  - **Ming Zhang**: mingzhang23@m.fudan.edu.cn

---

<p align="center">
  <b>Beyond Scaling</b> | Fudan NLP Lab
</p>
