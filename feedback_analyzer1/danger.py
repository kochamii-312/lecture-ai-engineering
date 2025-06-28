# danger.py
import re

def extract_dangerous_comments(comment_list):
    """
    危険コメント（誹謗中傷・違法・猥褻など）を抽出する関数

    Parameters:
        comment_list (List[str]): コメント文字列のリスト

    Returns:
        List[str]: 危険と判定されたコメント
    """

    # 危険ワード
    insult_words = [
        "バカ", "死ね", "アホ", "無能", "使えない", "きもい", "消えろ", "ゴミ", "頭おかしい",
        "意味不明", "日本語で喋れ", "は？", "マジでクズ", "くだらない", "ガイジ", "キチガイ"
    ]

    vulgar_words = [
        "殺す", "暴力", "性的", "レイプ", "セックス", "脱がす", "裸", "犯す", "違法", "薬物", "大麻"
    ]

    dangerous_comments = []

    for comment in comment_list:
        text = comment.lower()
        if any(word in text for word in insult_words + vulgar_words):
            dangerous_comments.append(comment)

    return dangerous_comments
