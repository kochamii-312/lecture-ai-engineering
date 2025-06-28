# importance.py
import re

def score_specificity(comment):
    score = 0
    if re.search(r'\d{1,3}(回目|ページ|講|スライド)', comment):
        score += 0.5
    if re.search(r'[A-Z][a-z]+|[a-zA-Z]{3,}', comment):  # 英語の技術用語や固有名詞
        score += 0.3
    if re.search(r'先生|講師|図|資料|内容', comment):
        score += 0.2
    return min(score, 1.0)

def score_urgency(comment):
    urgency_words = ['いただけるとありがたい', '期待します', 'わからない', '困る', '早急', '改善', 'すぐに', '対処', '不明', '曖昧']
    count = sum(word in comment for word in urgency_words)
    return min(count * 0.2, 1.0)

def score_commonality(cluster_size, total_comments):
    ratio = cluster_size / total_comments
    return min(ratio * 2, 1.0)  # 50%以上で1.0

def score_importance(spec, urg, comm):
    """
    合算して重要度スコアを計算する

    Parameters:
        spec (float): 具体性スコア (0.0 - 1.0)
        urg (float): 緊急性スコア (0.0 - 1.0)
        comm (float): 共通性スコア (0.0 - 1.0)

    Returns:
        float: 重要度スコア (0.0 - 10.0)
    """
    total_score = 10 * (0.3 * spec + 0.4 * urg + 0.3 * comm)
    return round(total_score, 1)

def get_cluster_number(comment, clustered):
    """
    特定のコメントに対応するクラスタ番号を返す

    Parameters:
        comment (str): 調べたいコメント
        clustered (List[Dict]): cluster_comments() の出力

    Returns:
        int or None: クラスタ番号（なければ None）
    """
    for item in clustered:
        if item["comment"] == comment:
            return item["cluster"]
    return None  # 該当コメントが見つからない場合

def get_cluster_size_and_total(cluster_number, clustered):
    """
    指定されたクラスタ番号のサイズと全体件数を返す

    Parameters:
        cluster_number (int): 対象のクラスタ番号
        clustered (List[Dict]): cluster_comments() の出力

    Returns:
        (int, int): (クラスタ内コメント数, 全体のコメント数)
    """
    cluster_size = sum(1 for item in clustered if item["cluster"] == cluster_number)
    total_comments = len(clustered)
    return cluster_size, total_comments
