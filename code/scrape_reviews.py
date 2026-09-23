import requests
import pandas as pd
import time
APP_ID = "1570093460"
COUNTRY = "us"
MAX_PAGES = 10


# =============================

def fetch_reviews(app_id, country, max_pages):
    all_reviews = []

    for page in range(1, max_pages + 1):
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
        print(f"正在抓取第 {page} 页...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                break
            data = response.json()
            entries = data.get("feed", {}).get("entry", [])
            if not entries or len(entries) == 0:
                break
            for entry in entries:
                if "im:rating" not in entry:
                    continue

                review = {
                    "rating": entry.get("im:rating", {}).get("label", ""),
                    "title": entry.get("title", {}).get("label", ""),
                    "content": entry.get("content", {}).get("label", ""),
                    "date": entry.get("updated", {}).get("label", ""),
                    "author": entry.get("author", {}).get("name", {}).get("label", "")
                }
                all_reviews.append(review)

        except Exception as e:
            print(f"第 {page} 页抓取失败: {e}")
            break

        time.sleep(1)

    return all_reviews

reviews = fetch_reviews(APP_ID, COUNTRY, MAX_PAGES)

if reviews:
    df = pd.DataFrame(reviews)
    df = df.dropna(subset=["content"])
    df = df[df["content"].str.strip() != ""]
    df.to_csv("reviews_us.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ 抓取完成！共获取 {len(df)} 条有效评论，已保存为 reviews_us_oldroll.csv")
    print("\n数据预览：")
    print(df.head())
else:
    print("❌ 没有抓取到任何评论，请检查 App ID 或网络。")