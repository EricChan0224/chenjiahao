# AI_Chat_Records.md

> 本文档汇总了完成三个挑战过程中，与 AI 助手（ChatGPT / Claude / Gemini）协作的关键对话链接。每条记录均附简短说明，标注该对话解决的核心问题。
>

---

## 任务一：基于大模型的中文病例实体抽取

- [https://gemini.google.com/share/d2564154cdf1](粘贴链接) —— 设计实体抽取 Prompt、调通 Qwen API 调用流程

---

## 任务二：心衰患者生存预测与 LaTeX 论文撰写 

​      # https://claude.ai/share/011f9ce9-368e-4343-b76e-5c6e61d59742

### 数据分析与建模
- [Notebook Cell 顺序排查] —— Cell 10 跑不通报 NameError 的根因定位（cell 物理顺序与逻辑顺序相反）及批量重排方法
- [结果可复现性与随机种子统一] —— 统一全局 `SEED`、修复变量名覆盖（`rf_model` 撞名）问题
- [Random Forest 类别权重调优] —— `class_weight='balanced'` → `'balanced_subsample'` 的尝试与效果验证
- [模型召回率差异排查] —— Logistic Regression 召回率高于 Random Forest 的原因分析、阈值调优方案讨论
- [Cell 10 新增 Random Forest 预测对比] —— 在新患者预测中加入 RF 模型，与 LR 结果并列对比

### 论文撰写与润色
- [论文数字与代码结果对齐] —— 用真实跑出的指标替换论文里的旧数字/占位数字，修正内部矛盾的表述
- [摘要质量检查与改写] —— 修正摘要中用词不准确（如 "highly interpretable"、"feature selection"）和过度主观化表述的问题
- [全文表述不清问题排查] —— 通读论文修正生造词、术语误用（如 "distance-based estimators"）等问题
- [第三危险因子补充] —— 根据 feature importance 图补充 age 作为第三个危险因子的论述

