# clustering.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

def summarize_comments(comment_list, n_summary=10):
    if len(comment_list) <= n_summary:
        return comment_list  # コメントが少なければそのまま返す

    # TF-IDFベースで文の特徴を数値化
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(comment_list)

    # KMeansでクラスタリング
    kmeans = KMeans(n_clusters=n_summary, random_state=0)
    kmeans.fit(X)

    # 各クラスタの代表的なコメントを選出
    summary = []
    for i in range(n_summary):
        cluster_indices = [j for j, label in enumerate(kmeans.labels_) if label == i]
        if cluster_indices:
            representative_idx = cluster_indices[0]
            summary.append(comment_list[representative_idx])
    return summary

def cluster_comments(comment_list, num_clusters=5):
    """
    コメントリストをクラスタリングし、クラスタ番号付きで返す関数
    
    Parameters:
        comment_list (List[str]): 文字列のコメントリスト
        num_clusters (int): クラスタ数

    Returns:
        List[Dict]: [{"comment": ..., "cluster": ...}, ...]
    """
    # 文章をベクトルに変換
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # 日本語対応
    embeddings = model.encode(comment_list)

    # KMeans でクラスタリング
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(embeddings)

    # コメントとクラスタ番号をペアにして返す
    result = [{"comment": c, "cluster": int(l)} for c, l in zip(comment_list, labels)]
    return result
