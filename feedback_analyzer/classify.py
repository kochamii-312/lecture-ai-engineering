# classify.py
import openai
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_comment(comment: str) -> dict:
    prompt = f"""
以下のコメントについて、以下の3つをJSON形式で出力してください：
1. sentiment: ポジティブ or ネガティブ
2. category: 講義内容 / 講義資料 / 運営 / その他
3. importance: 1〜5（重要なコメントほどスコアが高い）

コメント：
{comment}
    """.strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"エラー: {e}")
        return {"sentiment": "エラー", "category": "不明", "importance": 0}

def classify_comment_list(df):
    results = []
    for comment in df["comment"]:
        result = classify_comment(comment)
        results.append(result)
        time.sleep(0.3)  # API負荷軽減
    df["sentiment"] = [r["sentiment"] for r in results]
    df["category"] = [r["category"] for r in results]
    df["importance"] = [r["importance"] for r in results]
    return df
