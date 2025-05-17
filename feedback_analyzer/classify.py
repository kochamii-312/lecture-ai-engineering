# classify.py
import google.generativeai as genai
import os
import time
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-pro")

def classify_comment(comment: str) -> dict:
    prompt = f"""
    次のコメントに対して、以下の4つをJSON形式で出力してください：
    1. sentiment: "ポジティブ" または "ネガティブ"
    2. category: "講義内容", "講義資料", "運営", "その他" のいずれか
    3. danger_score: 危険性（0〜1の小数、0.1単位）
    4. importance_score: 重要性（0〜1の小数、具体性・緊急性・共通性を加味）

    コメント:
    """
    {comment}
    """
    """

    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text.strip())
        return result
    except Exception as e:
        print(f"エラー: {e}")
        return {
            "sentiment": "エラー",
            "category": "不明",
            "danger_score": 0,
            "importance_score": 0
        }

def analyze_comments(df: pd.DataFrame):
    results = []
    for comment in df["comment"]:
        results.append(classify_comment(comment))
        time.sleep(0.3)

    df["sentiment"] = [r["sentiment"] for r in results]
    df["category"] = [r["category"] for r in results]
    df["danger_score"] = [r["danger_score"] for r in results]
    df["importance_score"] = [r["importance_score"] for r in results]

    # 要約用（ポジ・ネガ）
    positive_summary = "\n".join(df[df["sentiment"] == "ポジティブ"]["comment"].head(10))
    negative_summary = "\n".join(df[df["sentiment"] == "ネガティブ"]["comment"].head(10))

    summaries = {
        "positive_summary": positive_summary,
        "negative_summary": negative_summary
    }

    return df, summaries