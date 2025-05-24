from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from labeling import get_sentiment_label
from main import df
from preprocess import split_into_sentences
from visualize import positive_comment_list, negative_comment_list

# メモ：ラベリングをその場でせず教師データから読み取る（yはカラム〇〇）
class SentimentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
    
    def train_on(self, comment_series):
        raw_comments = comment_series.drpona().tolist()    # 欠損値を削除, リスト化
        self.comments = split_into_sentences(raw_comments) # 文単位で分割
        self.train()

    def predict_on(self, comment_series):
        raw_comments = comment_series.dropna().tolist()
        self.comments = split_into_sentences(raw_comments)
        self.predict_and_store()

    def train(self):
        labels = [get_sentiment_label(c) for c in self.comments]

        # 特徴量とラベルの準備
        X = self.vectorizer.fit_transform(self.comments)
        y = labels

        # 学習
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        print(f"感情分類モデル精度: {self.model.score(X_test, y_test):.3f}")

    def predict_and_store(self):
        X = self.vectorizer.transform(self.comments)
        predicted_sentiments = self.model.predict(X)

        # 分類結果別でリストに格納
        for comment, sentiment in zip(self.comments, predicted_sentiments):
            if sentiment == "positive":
                positive_comment_list.append(comment)
            elif sentiment == "negative":
                negative_comment_list.append(comment)
            else:
                neutral_comment_list.appennd(comment)
    
    def get_results(self):
        return {
            "positive": positive_comment_list,
            "negative": negative_comment_list
        }