import os
import requests
import time
import pandas as pd
import MeCab
import matplotlib.pyplot as plt
from mlask import MLAsk
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_sentiment_label(comment):
    API_URL = "https://api-inference.huggingface.co/models/daigo/bert-base-japanese-sentiment"
    response = requests.post(API_URL, headers=headers, json={"inputs": comment})
    print(f"[DEBUG] Status Code: {response.status_code}")
    print(f"[DEBUG] Response Text: {response.text}")
    try:
        result = response.json()
        if isinstance(result, list):
            label = result[0][0]['label']
            return {
                "ポジティブ": "positive",
                "ネガティブ": "negative",
                "中立": "neutral"
            }.get(label, "neutral")
        else:
            return "neutral"
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON for: {comment[:30]}... → {e}")
        return "neutral"

# def get_sentiment_label(comment):
    """
    コメントを"positive", "negative", "neutral", "ironic"に分類
    日本語専用に訓練されたLLMベースの感情分類モデルdaigo/bert-base-japanese-sentiment-ironyを使用
    """
    # API_URL = "https://api-inference.huggingface.co/models/kit-nlp/bert-base-japanese-sentiment-irony"
    # print("HF_TOKEN: ", HF_TOKEN)
    # try:
    #     response = requests.post(API_URL, headers=headers, json={"inputs": comment})
    #     result = response.json()
    #     time.sleep(3)

    #     print(f"[DEBUG] API status: {response.status_code}")
    #     print(f"[DEBUG] API text: {response.text}")

    #     if isinstance(result, list):
    #         label = result[0][0]['label']
    #         return {
    #             "positive": "positive",
    #             "negative": "negative",
    #             "neutral": "neutral",
    #             "ironic": "negative"  # 皮肉をネガティブ扱いにマッピング
    #         }.get(label, "neutral")
    #     else:
    #         return "neutral"
    # except Exception as e:
    #     print(f"[ERROR] API failed for: {comment[:30]}... → {e}")
    #     print(f"[DEBUG] API status: {response.status_code}")
    #     print(f"[DEBUG] API text: {response.text}")
    #     return "neutral"
    
    # emotion_analyzer = MLAsk()
    # emotion_results = []
    # for comment_i in comment

def get_category_label(comment):
    """
    コメントを4つのカテゴリ「講義内容」「講義資料」「運営」「その他」に分類
    多言語対応(日本語含む)でゼロショット分類が得意なLLMベースのモデルXLM-RoBERTa-largeを使用
    """
    API_URL = "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli"
    candidate_labels = ["講義内容", "講義資料", "運営", "その他"]
    payload = {
        "inputs": comment,
        "parameters": {"candidate_labels": candidate_labels}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    time.sleep(3)
    if "labels" in result:
        return result["labels"][0] # 最もスコアの高いカテゴリ
    return "その他"

# embedding