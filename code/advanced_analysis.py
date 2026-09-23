import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# ========== 配置区 ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

FILE_PROCCD = os.path.join(BASE_DIR, "data", "raw", "reviews_us.csv")
FILE_DAZZ = os.path.join(BASE_DIR, "data", "raw", "reviews_dazzcam.csv")

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data(filepath, name):
    df = pd.read_csv(filepath).dropna(subset=['content', 'rating'])
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])
    df['content'] = df['content'].astype(str)
    df['app'] = name
    return df

df_pro = load_data(FILE_PROCCD, "ProCCD")
df_dazz = load_data(FILE_DAZZ, "Dazz Cam")
df_all = pd.concat([df_pro, df_dazz])

# ========== 模型一：评论长度与情绪投入度 ==========
print("正在分析用户情绪投入度...")
df_all['length'] = df_all['content'].apply(len)
df_all['sentiment_type'] = df_all['rating'].apply(lambda x: 'Positive (4-5)' if x >= 4 else ('Negative (1-2)' if x <= 2 else 'Neutral (3)'))

len_compare = df_all.groupby(['app', 'sentiment_type'])['length'].mean().unstack()

fig, ax = plt.subplots(figsize=(10, 6))
len_compare.plot(kind='bar', ax=ax, color=['#E74C3C', '#F39C12', '#2ECC71'])
plt.title('用户评论平均长度对比 (字数越多, 情绪投入越深)', fontsize=14)
plt.xlabel('产品', fontsize=12)
plt.ylabel('平均字符数', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='评论类型')
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, 'review_length_and_emotion.png'), dpi=150)
plt.close()
print("📊 评论长度与情绪投入度图已保存！")

# ========== 模型二：需求缺口提取 (Wish List) ==========
print("\n正在提取用户需求缺口 (Wish List)...")
def extract_wishes(df, name):
    # 匹配 wish/want/need/希望/想要 后面的名词短语
    pattern = re.compile(r'(?:wish|want|need|hope|could be better if|缺少|希望|建议|想要)\s+(.{0,40})', re.IGNORECASE)
    wishes = []
    for text in df['content']:
        matches = pattern.findall(text)
        for m in matches:
            # 清理标点符号和多余空格
            m = re.sub(r'[.,!?;:]', '', m).strip()
            if len(m) > 3 and len(m) < 30:
                wishes.append(m.lower())
    return Counter(wishes).most_common(10)

pro_wishes = extract_wishes(df_pro, "ProCCD")
dazz_wishes = extract_wishes(df_dazz, "Dazz Cam")

print("ProCCD 用户最想要的功能/改进：")
for w, c in pro_wishes:
    print(f"  - {w} ({c}次)")
print("\nDazz Cam 用户最想要的功能/改进：")
for w, c in dazz_wishes:
    print(f"  - {w} ({c}次)")

# ========== 模型三：痛点共现矩阵 (展示痛点如何导致负面行为) ==========
print("\n正在分析痛点共现关系...")
# 定义核心痛点词
pain_points = {
    '订阅/收费': ['subscription', 'subscribe', 'charged', 'charge', 'pay', 'payment', 'refund', 'cancel', 'vip', 'premium', 'price', 'expensive'],
    '广告/打断': ['ads', 'ad', 'advertisement', 'commercial', 'pop-up', 'popup', 'interrupt'],
    '稳定性': ['crash', 'freeze', 'bug', 'glitch', 'slow', 'lag', 'stuck', 'error'],
    '功能/质量': ['watermark', 'filter', 'quality', 'blur', 'fake', 'resolution', 'export', 'save']
}

# 计算每个产品中，痛点词之间的共现次数
co_occurrence_pro = {k: 0 for k in pain_points}
co_occurrence_dazz = {k: 0 for k in pain_points}

def count_co_occurrence(df):
    counts = Counter()
    for text in df['content'].str.lower():
        words = set(re.findall(r'\b[a-z]+\b', text))
        for cat, keywords in pain_points.items():
            if any(kw in words for kw in keywords):
                counts[cat] += 1
    return counts

pro_co = count_co_occurrence(df_pro)
dazz_co = count_co_occurrence(df_dazz)

# 画一个对比柱状图
categories = list(pain_points.keys())
pro_counts = [pro_co[c] for c in categories]
dazz_counts = [dazz_co[c] for c in categories]

x = range(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar([i - width/2 for i in x], pro_counts, width, label='ProCCD (光锥元)', color='#3498DB')
bars2 = ax.bar([i + width/2 for i in x], dazz_counts, width, label='Dazz Cam (竞品)', color='#E74C3C')

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylabel('提及该痛点的评论数量 (绝对数)', fontsize=12)
ax.set_title('核心痛点提及度对比 (绝对数量，直观展示双方短板)', fontsize=14)
ax.legend()

for bars in [bars1, bars2]:
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, 'painpoint_occurrence_compare.png'), dpi=150)
plt.close()
print("📊 核心痛点提及度对比图已保存！")

print("\n✅ 所有高级分析完成！图片已存入 images 文件夹。")