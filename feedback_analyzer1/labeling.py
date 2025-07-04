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

    positive_keywords = ['良かった', 'よかった', '良い', 'よい', 'ありがた', '有り難','やす', '楽しかった', '楽しい', '面白かった', '面白い', '素晴らしい', '素晴らしかった', '最高','嬉しい', '嬉しかった', '感謝', 'できた', '出来た', '良く', '助か', '満足','楽しみ', '丁寧', '親切', '役に立', '役立']
    negative_keywords = ['とまど', '戸惑', 'にく', 'づら', 'ずら','辛い','もうちょっと','ほしかった', 'もらいたかった','たら嬉しかった','ればよ','れば良','であるとよかった','ほうがいい', '方がいい', 'ほうが良い','方が良い', '方がよかった', 'ほうがよかった', 'であるとありがたかった', 'であると有難かった', '方がありがたかった', 'ほうがありがたかった', '方が有難かった', 'ほうが有難かった','わかりにくい', 'わかりづらい', '難しく', '難しすぎる', '難しすぎた', '難しかった', 'わからなかった', 'わからない', 'わかりません', '分からなかった', '分からない', '分かりません', '残念', 'できなかった','できない', 'できません', '出来ない','出来ません', 'いただけるとありがたい', '期待します']

    for neg_keyword in negative_keywords:
        if neg_keyword in text_lower:
            return 'negative'

    for pos_keyword in positive_keywords:
        if pos_keyword == 'よかった' and ('であるとよかった' or '方がよかった' or 'ほうがよかった') in text_lower:
            continue  # 'よかった'が'であるとよかった'の一部として含まれている場合はスキップ
        elif pos_keyword == '良かった' and ('であると良かった' or '方が良かった' or 'ほうが良かった') in text_lower:
            continue
        elif pos_keyword == 'よい' and ('であるとよい' or '方がよい' or 'ほうがよい' or 'あればよい') in text_lower:
            continue
        elif pos_keyword == '良い' and ('であると良い' or '方が良い' or 'ほうが良い' or 'あれば良い') in text_lower:
            continue
        elif pos_keyword == 'ありがたい' and ('であるとありがたい' or '方がありがたい' or 'ほうがありがたい' or 'いただけるとありがたい') in text_lower:
            continue
        elif pos_keyword == '有難い' and ('であると有難い' or '方が有難い' or 'ほうが有難い' or 'いただけると有難い') in text_lower:
            continue
        elif pos_keyword == 'ありがたかった' and ('であるとありがたかった' or '方がありがたかった' or 'ほうがありがたかった') in text_lower:
            continue
        elif pos_keyword == '嬉しかった' and ('であると嬉しかった' or 'たら嬉しかった') in text_lower:
            continue
        if pos_keyword in text_lower:
            return 'positive'

    return 'neutral'

def get_category_label(comment):
    rules = {
        "講義内容": ["内容", "説明", "理解", "わかりやすい", "話", "テーマ", "授業", "難し", "面白", "興味", "学び", "学習"],
        "講義資料": ["スライド", "資料", "図", "文字", "配布", "見え", "小さい"],
        "運営": ["時間", '休憩', "音", "声", "遅刻", "トラブル", "Zoom", "案内", "運営", "サポート", "質問", "進行", "対応", "連絡", "企画", "イベント", "公開", "開放"],
    }

    for category, keywords in rules.items():
        for word in keywords:
            if word in comment:
                return category
    return "その他"
