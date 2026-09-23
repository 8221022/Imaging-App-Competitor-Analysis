[README.md](https://github.com/user-attachments/files/32542301/README.md)
# 光锥元 ProCCD 海外用户洞察与竞品 Dazz Cam 对标及 GEO 截流策略

## 📌 项目背景
光锥元是一家面向欧美市场的 AI 影像出海公司。本项目以旗下 ProCCD（复古 CCD 相机 App）及其核心竞品 Dazz Cam 为分析对象，爬取美区 App Store 英文用户评论（合计 590+ 条），通过 Python 进行多维交叉分析，输出精准的 GEO 内容截流策略。

## 🛠️ 使用工具与数据
- **编程语言**：Python (Pandas, Matplotlib)
- **数据来源**：Apple App Store 美区公开 RSS 评论接口
- **样本规模**：ProCCD（90+ 条） vs 竞品 Dazz Cam（500 条）
- **分析方法**：痛点标签归类 + 情感长度分析（评论字数）+ 痛点共现模型

## 📊 核心发现（多维交叉验证）

### 1. 宏观口碑势均力敌，微观痛点截然不同
- **整体表现**：两款产品平均评分均为 **4.3 星**，好评率均在 **80%** 左右，产品基础体验难分伯仲。
- **痛点差异**：
  - **ProCCD 的核心危机是“信任危机”**：50% 的差评集中在“订阅扣费不透明”（如意外扣费、取消困难）。
  - **Dazz Cam 的核心危机是“体验危机”**：差评主要集中在 **广告太多/闪退严重**（占比 7.4%）。

### 2. 情感投入度分析（用户愤怒值）
- **ProCCD**：好评平均长度 180 字符，差评 117 字符。（说明喜欢的人极其热爱，写长文称赞滤镜质感）
- **Dazz Cam**：差评平均长度 **195 字符**，好评 146 字符。（说明竞品用户因广告/闪退问题积累了极大的愤怒和不满）
- **业务洞察**：Dazz Cam 的用户愤怒值极高，流失意愿强烈，这为我们截流其高净值用户提供了绝佳的切入时机。

### 3. 竞品痛点软肋（人工阅读提取）
- **广告打断创作**：高频出现诸如 *"I can't even apply a filter without watching a 30-second ad."* 这样的抱怨，说明广告严重影响了核心创作体验。
- **稳定性堪忧**：大量用户反馈闪退频繁，导致拍摄瞬间流失。


## 💡 GEO / SEO 优化策略
基于以上数据，建议采取“避其锋芒，攻其软肋”的组合策略：

**策略1：进攻——截流竞品流失用户**
针对 Dazz Cam “广告太多”的弱点，在 Reddit、Quora 等海外平台布局结构化长尾内容：
- *"Best no-ads retro camera app alternatives"*
- *"Dazz Cam too many ads? Try these stable alternatives"*
重点突出 ProCCD 的“无广告打断、稳定不闪退、专业复古质感”，精准吸引愿意为品质付费的高净值用户。

**策略2：防守——化解自身信任危机**
针对 ProCCD “订阅扣费不透明”的痛点，在 SEO 内容中主动布局透明化 FAQ：
- *"Is ProCCD subscription worth it? A transparent review"*
- *"How to cancel ProCCD subscription?"*
用坦诚的沟通降低预期落差，缓解用户的“被欺骗感”。

**策略3：场景化拦截——抢占即时搜索需求**
围绕“旅行、探店、音乐节”等拍照场景，创作教程类内容：
- *"How to get vintage film look on iPhone"*
- *"Best retro camera app for travel photography"*

## 📁 项目结构说明
- `code/`：Python 爬虫与分析代码
- `data/raw/`：原始评论数据（ProCCD & Dazz Cam）
- `images/`：数据可视化图表（星级分布、情感长度、痛点对比）
- `光锥元 ProCCD 海外用户洞察与竞品 Dazz Cam 对标及 GEO 截流策略.pdf`：完整版分析报告

## ⚠️ 开发踩坑日志（Dev Log）
本项目在开发过程中遇到并解决了以下真实技术问题：
1. **样本偏差处理**：由于 App Store 接口限制，ProCCD 样本量（90+条）小于 Dazz Cam（500条）。因此本分析**拒绝绝对数量对比**，采用“差评比例对比”与“情感长度分析”来消除样本偏差。
2. **交叉验证**：本人亲自下载了 ProCCD 进行实测，验证了产品痛点确实集中在订阅机制，而非广告体验。

---
> 本项目为个人求职作品集，旨在展示“数据驱动内容运营”的分析思维与实践能力。欢迎交流指正。
