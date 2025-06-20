from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from preprocess import split_into_sentences
from labeling import get_category_label
from comment_lists import lecture_content_comment_list, lecture_materials_comment_list, operation_comment_list, others_comment_list

# メモ：ラベリングをその場でせず教師データから読み取る（yはカラム〇〇）
class CategoryClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
    
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
        labels = [get_category_label(c) for c in self.comments]

        # 特徴量とラベルの準備
        X = self.vectorizer.fit_transform(self.comments)
        y = labels

        # 学習
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        print(f"カテゴリ分類モデル精度: {self.model.score(X_test, y_test):.3f}")

    def predict_and_store(self):
        X = self.vectorizer.transform(self.comments)
        predicted_categories = self.model.predict(X)

        for comment, cat in zip(self.comments, predicted_categories):
            if cat == "講義内容":
                lecture_content_comment_list.append(comment)
            elif cat == "講義資料":
                lecture_materials_comment_list.append(comment)
            elif cat == "運営":
                operation_comment_list.append(comment)
            else:
                others_comment_list.append(comment)
    
    def get_results(self):
        return {
            "講義内容": lecture_content_comment_list,
            "講義資料": lecture_materials_comment_list,
            "運営": operation_comment_list,
            "その他": others_comment_list
        }