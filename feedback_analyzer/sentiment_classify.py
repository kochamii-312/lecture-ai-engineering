from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from labeling import get_sentiment_label
from main import df
from preprocess import split_into_sentences
from visualize import positive_comment_list, negative_comment_list

def sentiment_classify(column_name):

    # 欠損値を削除, リスト化, 文単位で分割
    comments = split_into_sentences(df[column_name].dropna().tolist())

    sentiments = [get_sentiment_label(c) for c in comments]

    df_filtered = df.loc[df[column_name].notna()].copy()
    df_filtered['sentiment'] = sentiments

    vectorizer_sent = TfidfVectorizer()
    X_sent = vectorizer_sent.fit_transform(comments)
    y_sent = df_filtered['sentiment']

    X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_sent, y_sent, test_size=0.2, random_state=42)
    logreg = LogisticRegression(max_iter=1000)
    logreg.fit(X_train_s, y_train_s)

    print(f"感情分類モデル精度: {logreg.score(X_test_s, y_test_s):.3f}")

    # 分類結果別でリストに格納
    predicted_sentiments = logreg.predict(X_sent)

    for comment, sent in zip(comments, predicted_sentiments):
        if sent == "positive":
            positive_comment_list.append(comment)
        elif sent == "negative":
            negative_comment_list.append(comment)   
