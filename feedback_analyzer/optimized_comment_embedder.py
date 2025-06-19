import time
import requests

class OptimizedCommentEmbedder:
    def __init__(self, hf_token, batch_size=32):
        self.hf_token = hf_token
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        self.batch_size = batch_size
        self._cache = {}  # 結果キャッシュ
    
    def get_embeddings_batch(self, texts):
        """バッチ処理で埋め込みを取得"""
        embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            
            # キャッシュチェック
            uncached_texts = []
            batch_embeddings = []
            
            for text in batch:
                if text in self._cache:
                    batch_embeddings.append(self._cache[text])
                else:
                    uncached_texts.append(text)
            
            # 未キャッシュのテキストをAPIで処理
            if uncached_texts:
                try:
                    api_url = "https://api-inference.huggingface.co/intfloat/multilingual-e5-small"
                    response = requests.post(
                        api_url, 
                        headers=self.headers, 
                        json={"inputs": uncached_texts},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        new_embeddings = response.json()
                        
                        # キャッシュに保存
                        for text, embedding in zip(uncached_texts, new_embeddings):
                            self._cache[text] = embedding
                            batch_embeddings.append(embedding)
                    else:
                        # エラー時はゼロベクトルで代替
                        zero_vector = [0.0] * 384  # multilingual-e5-smallの次元数
                        batch_embeddings.extend([zero_vector] * len(uncached_texts))
                        
                except Exception as e:
                    print(f"API Error: {e}")
                    # エラー時の代替処理
                    zero_vector = [0.0] * 384
                    batch_embeddings.extend([zero_vector] * len(uncached_texts))
            
            embeddings.extend(batch_embeddings)
            
            # レート制限対策
            time.sleep(0.1)
        
        return embeddings