from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

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
