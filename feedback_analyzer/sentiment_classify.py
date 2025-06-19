from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from labeling import get_sentiment_label
from main import df
from preprocess import split_into_sentences
from visualize import positive_comment_list, negative_comment_list, neutral_comment_list

# メモ：ラベリングをその場でせず教師データから読み取る（yはカラム〇〇）
class SentimentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.positive_comments = []
        self.negative_comments = []
        self.neutral_comments = []
    
    def train_on(self, comment_series):
        raw_comments = comment_series.dropna().tolist()  # 修正: drpona → dropna
        self.comments = split_into_sentences(raw_comments)
        self.train()

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
                self.neutral_comments.append(comment)  # 修正: appennd → append
    def get_results(self):
        return {
            "positive": positive_comment_list,
            "negative": negative_comment_list
        }