import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_sentiment_label(comment):
    """
    コメントを"positive", "negative", "neutral", "ironic"に分類
    日本語専用に訓練されたLLMベースの感情分類モデルdaigo/bert-base-japanese-sentiment-ironyを使用
    """
    API_URL = "https://api-inference.huggingface.co/kit-nlp/bert-base-japanese-sentiment-irony"
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": comment})
        result = response.json()

        if isinstance(result, list):
            label = result[0][0]['label']
            return {
                "positive": "positive",
                "negative": "negative",
                "neutral": "neutral",
                "ironic": "negative"  # 皮肉をネガティブ扱いにマッピング
            }.get(label, "neutral")
        else:
            return "neutral"
    except Exception as e:
        print(f"[ERROR] API failed for: {comment[:30]}... → {e}")
        return "neutral"

def get_category_label(comment):
    """
    コメントを4つのカテゴリ「講義内容」「講義資料」「運営」「その他」に分類
    多言語対応(日本語含む)でゼロショット分類が得意なLLMベースのモデルXLM-RoBERTa-largeを使用
    """
    API_URL = "https://api-inference.huggingface.co/joeddav/xlm-roberta-large-xnli"
    candidate_labels = ["講義内容", "講義資料", "運営", "その他"]
    payload = {
        "inputs": comment,
        "parameters": {"candidate_labels": candidate_labels}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    if "labels" in result:
        return result["labels"][0] # 最もスコアの高いカテゴリ
    return "その他"

# embedding