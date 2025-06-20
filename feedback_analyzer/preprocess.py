# preprocess.py
import pandas as pd
import re

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
        if not isinstance(comment, str):  # ← 安全チェック追加
            continue
        # 「。」や「！」改行などで分割（必要に応じて追加）
        sentences = re.split(r'[。．!?\n]', comment)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:  # 空文字は除外
                sentence_list.append(sentence)
    return sentence_list

def merge_comment_columns(df, column_names, sep=" "):
    """
    複数のカラムを1つのリストにまとめる関数
    Parameters:
        df (pd.DataFrame): 元のデータフレーム
        column_names (list of str): 結合対象のカラム名リスト
        sep (str): 各カラム間の区切り文字（デフォルトは空白）

    Returns:
        list of str: 各行を結合した1つのリスト
    """
    merged_list = []
    for _, row in df[column_names].dropna(how="all").iterrows():
        values = [str(row[col]).strip() for col in column_names if pd.notna(row[col])]
        if values:
            merged_list.append(sep.join(values))
    return merged_list
