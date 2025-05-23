from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from main import df
from preprocess import split_into_sentences
from labeling import get_category_label
from visualize import lecture_content_comment_list, lecture_materials_comment_list, operation_comment_list, others_comment_list

def category_classify(column_name):
    
    # 欠損値を削除, リスト化, 文単位で分割
    comments = split_into_sentences(df[column_name].dropna().tolist())

    categories = [get_category_label(c) for c in comments]

    df_filtered = df.loc[df[column_name].notna()].copy()
    df_filtered['category'] = categories

    vectorizer_cat = TfidfVectorizer()
    X_cat = vectorizer_cat.fit_transform(comments)
    y_cat = df_filtered['category']

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cat, y_cat, test_size=0.2, random_state=42)
    nb = MultinomialNB()
    nb.fit(X_train_c, y_train_c)

    print(f"カテゴリ分類モデル精度: {nb.score(X_test_c, y_test_c):.3f}")

    predicted_categories = nb.predict(X_cat)

    for comment, cat in zip(comments, predicted_categories):
        if cat == "講義内容":
            lecture_content_comment_list.append(comment)
        elif cat == "講義資料":
            lecture_materials_comment_list.append(comment)
        elif cat == "運営":
            operation_comment_list.append(comment)
        else:
            others_comment_list.append(comment)