import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from labeling import get_sentiment_label
from preprocess import split_into_sentences
from comment_lists import positive_comment_list, negative_comment_list, neutral_comment_list

# メモ：ラベリングをその場でせず教師データから読み取る（yはカラム〇〇）
class SentimentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.positive_comments = []
        self.negative_comments = []
        self.neutral_comments = []
    
    def train_on(self, comment_list):
        # NaNや空文字を除去
        clean_comments = [c for c in comment_list if isinstance(c, str) and c.strip()]
        self.comments = split_into_sentences(clean_comments)
        self.train()

    def predict_on(self, comment_list):
        # NaNや空文字を除去
        clean_comments = [c for c in comment_list if isinstance(c, str) and c.strip()]
        self.comments = split_into_sentences(clean_comments)
        self.predict_and_store()

    def train(self):
        if not self.comments:
            st.warning("⚠️ 学習用コメントが空です。train() をスキップします。")
            print("学習用コメントが空")
            return

        print("train()が始まった")
        labels = [get_sentiment_label(comment) for comment in self.comments]
        print("labels: ", labels)

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

        # 結果をインスタンス変数に格納
        for comment, sentiment in zip(self.comments, predicted_sentiments):
            if sentiment == "positive":
                self.positive_comments.append(comment)
            elif sentiment == "negative":
                self.negative_comments.append(comment)
            else:
                self.neutral_comments.append(comment)
    
    def get_results(self):
        return {
            "positive": positive_comment_list,
            "negative": negative_comment_list
        }