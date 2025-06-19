import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances

class CommentEmbedder:
    def __init__(self, hf_token):
        """
        Hugging Face APIを使ってコメント埋め込み・類似度・クラスタ分析を行うクラス
        """
        self.hf_token = hf_token
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}

    def get_embedding(self, text):
        """
        1つのテキストから埋め込みベクトルを取得
        """
        api_url = "https://api-inference.huggingface.co/intfloat/multilingual-e5-small"
        response = requests.post(api_url, headers=self.headers, json={"inputs": text})
        embedding = response.json()
        return embedding[0] if isinstance(embedding, list) else embedding

    def get_embeddings(self, texts):
        """
        複数のテキストを埋め込みベクトルに変換
        """
        return [self.get_embedding(text) for text in texts]

    def compute_similarity_matrix(self, embeddings):
        """
        埋め込みベクトル間のコサイン類似度行列を計算
        """
        return cosine_similarity(embeddings)

    def find_similar_pairs(self, texts, threshold=0.85):
        """
        類似度がしきい値以上のコメントペアを抽出
        """
        embeddings = self.get_embeddings(texts)
        sim_matrix = self.compute_similarity_matrix(embeddings)
        similar_pairs = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if sim_matrix[i, j] > threshold:
                    similar_pairs.append((texts[i], texts[j], sim_matrix[i, j]))
        return similar_pairs
    
    def cluster_comments(self, texts, n_clusters=10):
        """
        コメントをクラスタリングして、クラスタIDごとに分けて返す
        """
        embeddings = self.get_embeddings(texts)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        clusters = {i: [] for i in range(n_clusters)}
        for text, label in zip(texts, labels):
            clusters[label].append(text)
        return clusters
    
    def summarize_cluster(self, cluster_texts):
        """
        複数の文(クラスタ)を結合してHugging FaceのAPIで要約する
        """
        api_url = "https://api-inference.huggingface.co/csebuetnlp/mT5_multilingual_XLSum"
        input_text = " ".join(cluster_texts)

        response = requests.post(api_url, headers=self.headers, json={"inputs": input_text})
        result = response.json()
        return result[0]['summary_text'] if isinstance(result, list) and 'summary_text' in result[0] else "（要約失敗）"
    
    def cluster_and_rank(self, texts, n_clusters=10):
        """
        コメントをクラスタリングして件数と代表文をまとめたcluster_summaryを返す
        """
        embeddings = self.get_embeddings(texts)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(embeddings)
        labels = kmeans.labels_

        # クラスタごとの件数と代表文（重心に最も近い文）
        cluster_summary = []
        for i in range(n_clusters):
            indices = np.where(labels == i)[0]
            cluster_texts = [texts[idx] for idx in indices]
            cluster_embeddings = [embeddings[idx] for idx in indices]

            # 中心と最も近い文を代表に
            center = kmeans.cluster_centers_[i]
            distances = cosine_distances(cluster_embeddings, [center])
            rep_idx = distances.argmin()
            representative = cluster_texts[rep_idx]

            cluster_summary.append((len(cluster_texts), representative))

        # 件数順にソートして返す
        cluster_summary.sort(reverse=True, key=lambda x: x[0])
        return cluster_summary