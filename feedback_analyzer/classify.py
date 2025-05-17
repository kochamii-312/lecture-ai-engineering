# classify.py (Hugging Face版)
import os
import time
import json
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"  # 多クラス分類＋ゼロショットに強いモデル

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_huggingface(texts, labels):
    inputs = [{
        "inputs": text,
        "parameters": {
            "candidate_labels": labels,
            "multi_label": True
        }
    } for text in texts]

    results = []
    for payload in inputs:
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload)
            result = response.json()
            results.append(result)
        except Exception as e:
            print("[ERROR]", e)
            results.append({})
        time.sleep(1.0)  # rate limit 対策
    return results

def analyze_comments(df: pd.DataFrame):
    texts = df["comment"].tolist()

    # 感情分類（ポジ/ネガ）
    sentiment_results = query_huggingface(texts, ["ポジティブ", "ネガティブ"])
    categories_results = query_huggingface(texts, ["講義内容", "講義資料", "運営", "その他"])

    sentiments = []
    categories = []

    for sent_r, cat_r in zip(sentiment_results, categories_results):
        try:
            sentiments.append(max(zip(sent_r["scores"], sent_r["labels"]))[1])
        except:
            sentiments.append("不明")
        try:
            categories.append(max(zip(cat_r["scores"], cat_r["labels"]))[1])
        except:
            categories.append("その他")

    df["sentiment"] = sentiments
    df["category"] = categories

    # ダミーのスコア（後でローカルモデル/関数化可能）
    df["danger_score"] = [0.1 + 0.1 * ("怒" in c or "最悪" in c) for c in texts]
    df["importance_score"] = [min(1.0, 0.1 * len(c.split("。"))) for c in texts]

    positive_summary = "\n".join(df[df["sentiment"] == "ポジティブ"]["comment"].head(10))
    negative_summary = "\n".join(df[df["sentiment"] == "ネガティブ"]["comment"].head(10))

    summaries = {
        "positive_summary": positive_summary,
        "negative_summary": negative_summary
    }

    return df, summaries
