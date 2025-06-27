# labeling.py

def get_sentiment_label(comment):
    """
    コメントの感情ラベルを取得する関数
    Parameter:
        comment: コメント
    Returns:
        'positive', 'negative', または 'neutral' based
    """
    if not isinstance(comment, str):
        return 'neutral'

    text_lower = comment.lower()

    positive_keywords = ['良かった', 'よかった', '良い', 'よい', 'ありがとうござい', '有難うござい', 'やす', '楽しかった', '楽しい', '面白かった', '面白い', '素晴らしい', '素晴らしかった', '最高','嬉しい', '嬉しかった', '感謝', 'できた', '出来た', 'よく', '良く', '助か', '満足']
    negative_keywords = ['気にな', 'とまど', '戸惑', 'にく', 'づら', 'ずら','もうちょっと', 'であるとよかった', '方がよかった', 'ほうがよかった', 'であるとありがたかった', 'であると有難かった', '方がありがたかった', 'ほうがありがたかった', '方が有難かった', 'ほうが有難かった','わかりにくい', 'わかりづらい', '難しい', '難しすぎる', '難しすぎた', '難しかった', 'わからなかった', 'わからない', '分からなかった', '分からない']

    for neg_keyword in negative_keywords:
        if neg_keyword in text_lower:
            return 'negative'

    for pos_keyword in positive_keywords:
        if pos_keyword == 'よかった' and ('であるとよかった' or '方がよかった' or 'ほうがよかった') in text_lower:
            continue  # 'よかった'が'であるとよかった'の一部として含まれている場合はスキップ
        elif pos_keyword == '良かった' and ('であると良かった' or '方が良かった' or 'ほうが良かった') in text_lower:
            continue
        elif pos_keyword == 'よい' and ('であるとよい' or '方がよい' or 'ほうがよい') in text_lower:
            continue
        elif pos_keyword == '良い' and ('であると良い' or '方が良い' or 'ほうが良い') in text_lower:
            continue
        if pos_keyword in text_lower:
            return 'positive'

    return 'neutral'

