import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# ================= 配置区 =================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
import os

# 自动获取项目根目录，并在其下创建名为 'images' 的文件夹
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True) # 如果没有这个文件夹，Python会自动帮你建！
# 确保这两个文件在当前文件夹里！
FILE_PROCCD = r"C:\Users\whyhyy\PycharmProjects\Proccd_commodity_compare\data\raw\reviews_us.csv"
FILE_DAZZ = r"C:\Users\whyhyy\PycharmProjects\Proccd_commodity_compare\data\raw\reviews_dazzcam.csv"
# ==========================================

def load_and_clean(filepath, app_name):
    df = pd.read_csv(filepath)
    df = df.dropna(subset=['content'])
    df = df[df['content'].astype(str).str.strip() != '']
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])
    df['app_name'] = app_name
    return df

def classify_painpoint(row):
    text = (str(row["title"]) + " " + str(row["content"])).lower()
    if any(k in text for k in ["subscription", "charged", "refund", "pay", "premium", "expensive", "cancel", "vip"]):
        return "订阅/收费问题"
    if any(k in text for k in ["ads", "advertisement", "ad "]):
        return "广告太多"
    if any(k in text for k in ["freeze", "crash", "bug", "slow", "glitch", "闪退", "卡顿"]):
        return "闪退/卡顿"
    if any(k in text for k in ["fake", "filter", "watermark", "quality", "滤镜", "水印"]):
        return "滤镜/水印"
    return "其他"

# 1. 读取数据
print("正在读取数据...")
df_pro = load_and_clean(FILE_PROCCD, "ProCCD (光锥元)")
df_dazz = load_and_clean(FILE_DAZZ, "Dazz Cam (竞品)")
print(f"✅ ProCCD 有效评论: {len(df_pro)} 条")
print(f"✅ Dazz Cam 有效评论: {len(df_dazz)} 条")

# 2. 提取差评并分类
def analyze_painpoints(df):
    bad = df[df['rating'] <= 3].copy()
    bad['category'] = bad.apply(classify_painpoint, axis=1)
    counts = bad['category'].value_counts()
    # 转为百分比，消除样本量差异！
    percentages = (counts / len(bad) * 100).round(1)
    return percentages

pro_pain = analyze_painpoints(df_pro)
dazz_pain = analyze_painpoints(df_dazz)

print("\n📊 ProCCD 差评原因占比：")
for cat, pct in pro_pain.items():
    print(f"  {cat}: {pct}%")
print("\n📊 Dazz Cam 差评原因占比：")
for cat, pct in dazz_pain.items():
    print(f"  {cat}: {pct}%")

# 3. 绘制高逼格的痛点对比图（百分比对比）
categories = ['订阅/收费问题', '广告太多', '闪退/卡顿', '滤镜/水印']
pro_values = [pro_pain.get(c, 0) for c in categories]
dazz_values = [dazz_pain.get(c, 0) for c in categories]

x = range(len(categories))
width = 0.35

plt.figure(figsize=(10, 6))
bars1 = plt.bar([i - width/2 for i in x], pro_values, width, label='ProCCD (光锥元)', color='#4A90E2')
bars2 = plt.bar([i + width/2 for i in x], dazz_values, width, label='Dazz Cam (竞品)', color='#E74C3C')

for bars in [bars1, bars2]:
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}%', ha='center', va='bottom', fontsize=11)

plt.xticks(x, categories, fontsize=12)
plt.ylabel('Percentage of Negative Reviews (%)', fontsize=12)
plt.title('Negative Review Pain Points: ProCCD vs Dazz Cam', fontsize=14)
plt.legend()
plt.tight_layout()
save_path = os.path.join(IMAGE_DIR, 'competitor_painpoints_comparison.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight')
print(f"📊 最终对比图已保存至: {save_path}")
print("\n📊 最终对比图已保存！")

# 4. 提取好评场景词（升级维度！）
def get_top_words(df, top_n=15):
    pos = df[df['rating'] >= 4]
    text = ' '.join(pos['content'].astype(str).str.lower())
    words = re.findall(r'\b[a-z]{4,}\b', text)
    stopwords = set(['this', 'that', 'with', 'have', 'they', 'from', 'what', 'when', 'just', 'like', 'good', 'great', 'love', 'really', 'very', 'much', 'make', 'made', 'would', 'could', 'there', 'their', 'about', 'them', 'then', 'were', 'been', 'been', 'your', 'will', 'even', 'some', 'only', 'also', 'into', 'more', 'most', 'over', 'after', 'these', 'other', 'app', 'camera'])
    filtered = [w for w in words if w not in stopwords]
    return Counter(filtered).most_common(top_n)

print("\n👍 ProCCD 好评高频场景词（用户画像）：")
print(get_top_words(df_pro))
print("\n👍 Dazz Cam 好评高频场景词：")
print(get_top_words(df_dazz))

import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from wordcloud import WordCloud

# ========== 配置区 ==========
# 自动找到你的 images 文件夹
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

FILE_PROCCD = os.path.join(BASE_DIR, "data", "raw", "reviews_us.csv")
FILE_DAZZ = os.path.join(BASE_DIR, "data", "raw", "reviews_dazzcam.csv")

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 读取数据 ==========
df_pro = pd.read_csv(FILE_PROCCD).dropna(subset=['content', 'rating'])
df_dazz = pd.read_csv(FILE_DAZZ).dropna(subset=['content', 'rating'])
df_pro['rating'] = pd.to_numeric(df_pro['rating'], errors='coerce')
df_dazz['rating'] = pd.to_numeric(df_dazz['rating'], errors='coerce')

# ========== 图表1：星级分布对比图 ==========
fig, ax = plt.subplots(figsize=(8, 5))
pro_stars = df_pro['rating'].value_counts().sort_index()
dazz_stars = df_dazz['rating'].value_counts().sort_index()

x = range(1, 6)
width = 0.35

# 计算各自的占比（因为样本量不同，用占比更科学）
pro_pct = [(pro_stars.get(i, 0) / len(df_pro)) * 100 for i in x]
dazz_pct = [(dazz_stars.get(i, 0) / len(df_dazz)) * 100 for i in x]

ax.bar([i - width / 2 for i in x], pro_pct, width, label='ProCCD (光锥元)', color='#4A90E2')
ax.bar([i + width / 2 for i in x], dazz_pct, width, label='Dazz Cam (竞品)', color='#E74C3C')

ax.set_xticks(x)
ax.set_xticklabels(['1星', '2星', '3星', '4星', '5星'], fontsize=12)
ax.set_ylabel('占比 (%)', fontsize=12)
ax.set_title('星级评分分布对比 (ProCCD vs Dazz Cam)', fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, 'star_distribution_compare.png'), dpi=150, bbox_inches='tight')
plt.close()
print("📊 星级分布对比图已保存！")


# ========== 图表2：好评与差评词云图 ==========
def generate_wordcloud(df, app_name):
    pos_text = ' '.join(df[df['rating'] >= 4]['content'].astype(str)).lower()
    neg_text = ' '.join(df[df['rating'] <= 2]['content'].astype(str)).lower()

    stopwords = set(
        ['the', 'and', 'for', 'this', 'that', 'with', 'you', 'but', 'not', 'are', 'was', 'have', 'has', 'app', 'it',
         'is', 'to', 'of', 'in', 'on', 'my', 'me', 'so', 'very', 'just', 'can', 'if', 'get', 'all', 'be', 'i', 'a',
         'an', 'good', 'great', 'love', 'like', 'use', 'using', 'used', 'would', 'make', 'made', 'really', 'much',
         'want', 'even', 'ever', 'still', 'there', 'dont', 'cant', 'its', 'youre', 'im', 'ive', 'had', 'her', 'him',
         'she', 'he', 'they', 'we', 'our', 'your', 'their', 'them'])

    def clean(text):
        words = re.findall(r'\b[a-z]{3,}\b', text)
        return ' '.join([w for w in words if w not in stopwords])

    pos_clean = clean(pos_text)
    neg_clean = clean(neg_text)

    # 画好评词云
    if pos_clean.strip():
        wc_pos = WordCloud(width=800, height=400, background_color='white', max_words=50).generate(pos_clean)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_pos, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'{app_name} - 好评高频词', fontsize=16)
        plt.savefig(os.path.join(IMAGE_DIR, f'wordcloud_{app_name}_good.png'), dpi=150, bbox_inches='tight')
        plt.close()

    # 画差评词云
    if neg_clean.strip():
        wc_neg = WordCloud(width=800, height=400, background_color='black', colormap='Reds', max_words=50).generate(
            neg_clean)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_neg, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'{app_name} - 差评高频词', fontsize=16)
        plt.savefig(os.path.join(IMAGE_DIR, f'wordcloud_{app_name}_bad.png'), dpi=150, bbox_inches='tight')
        plt.close()


generate_wordcloud(df_pro, 'ProCCD')
generate_wordcloud(df_dazz, 'DazzCam')
print("📊 好评与差评词云图已保存！")

# ========== 图表3：评论长度对比（愤怒值洞察） ==========
df_pro['length'] = df_pro['content'].apply(lambda x: len(str(x)))
df_dazz['length'] = df_dazz['content'].apply(lambda x: len(str(x)))

pro_avg_len_good = df_pro[df_pro['rating'] >= 4]['length'].mean()
pro_avg_len_bad = df_pro[df_pro['rating'] <= 2]['length'].mean()
dazz_avg_len_good = df_dazz[df_dazz['rating'] >= 4]['length'].mean()
dazz_avg_len_bad = df_dazz[df_dazz['rating'] <= 2]['length'].mean()

fig, ax = plt.subplots(figsize=(8, 5))
labels = ['ProCCD\n好评', 'ProCCD\n差评', 'DazzCam\n好评', 'DazzCam\n差评']
values = [pro_avg_len_good, pro_avg_len_bad, dazz_avg_len_good, dazz_avg_len_bad]
colors = ['#2ECC71', '#E74C3C', '#2ECC71', '#E74C3C']

bars = ax.bar(labels, values, color=colors)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval:.0f} 字符', ha='center', va='bottom', fontsize=11)

ax.set_ylabel('平均评论长度 (字符数)', fontsize=12)
ax.set_title('用户评论长度对比 (反映用户情绪投入度)', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, 'review_length_compare.png'), dpi=150, bbox_inches='tight')
plt.close()
print("📊 评论长度对比图已保存！")