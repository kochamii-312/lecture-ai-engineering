# preprocess.py
import re

def split_into_sentences(comment_list):
    """
    各要素に複数文含むリストを受け取り、「。」や「！」改行などで分割して新しいリストを返す関数
    Parameters:
        comment_list (list of str): 元のコメントリスト（各要素に複数文が含まれることがある）
    Returns:
        list of str: すべての文を1文ずつ展開した新しいリスト
    """
    sentence_list = []
    for comment in comment_list:
        if not isinstance(comment, str):
            continue  # コメントが文字列でない場合(Nan等)はスキップ
        sentences = re.split(r'(?:[。．・！？!?]+(?:\\n|\n)?|\\n)', comment)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:  # 空文字は除外
                sentence_list.append(sentence)
    return sentence_list