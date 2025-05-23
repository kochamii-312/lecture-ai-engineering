# preprocess.py
import pandas as pd
import re
import openai # embeddingに使っている
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"  # 多クラス分類＋ゼロショットに強いモデル

headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def split_into_sentences(comment_list):
    """
    各要素に複数文含むリストを受け取り、文単位で分割して新しいリストを返す関数
    
    Parameters:
        comment_list (list of str): 元のコメントリスト（各要素に複数文が含まれることがある）

    Returns:
        list of str: すべての文を1文ずつ展開した新しいリスト
    """
    sentence_list = []
    for comment in comment_list:
        # 「。」や改行などで分割（必要に応じて追加可能）
        sentences = re.split(r'[。．\n]', comment)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:  # 空文字は除外
                sentence_list.append(sentence)
    return sentence_list

def merge_comment_columns(df):
    """
    複数行のデータを1行にまとめる関数
    今は使っていないが一応取っておく
    """
    comment_columns = [
        "特に良かった点",
        "わかりにくかった部分や改善点",
        "講師についてよかった点や不満があった点",
        "今後開講してほしい講義・分野など",
        "自由に意見"
    ]
    all_comments = []

    for _, row in df.iterrows():
        for col in comment_columns:
            text = str(row.get(col, "")).strip()
            if text:
                all_comments.append({
                    "original_column": col,
                    "comment": text
                })

    return pd.DataFrame(all_comments)

def get_embedding(text):
    response = openai.Embedding.create(
        model="test-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']