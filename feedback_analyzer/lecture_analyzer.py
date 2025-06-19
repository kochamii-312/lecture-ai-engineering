import streamlit as st
from optimized_comment_embedder import OptimizedCommentEmbedder
from sentiment_classify import SentimentClassifier
from category_classify import CategoryClassifier
from analysis_results import AnalysisResults

class LectureAnalyzer:
    def __init__(self, hf_token):
        self.hf_token = hf_token
        self.embedder = OptimizedCommentEmbedder(hf_token)
        self.sentiment_classifier = SentimentClassifier()
        self.category_classifier = CategoryClassifier()
        self.results = None
    
    def analyze(self, df, train_df=None):
        """総合分析を実行"""
        try:
            # データ前処理
            comment_columns = self._identify_comment_columns(df)
            all_comments = self._extract_comments(df, comment_columns)
            
            # 訓練データがある場合は学習
            if train_df is not None:
                self._train_models(train_df)
            
            # 分析実行
            sentiment_results = self._analyze_sentiment(all_comments)
            category_results = self._analyze_categories(all_comments)
            dangerous_comments = self._detect_dangerous_comments(all_comments)
            
            # 結果をまとめる
            self.results = AnalysisResults(
                positive_comments=sentiment_results['positive'],
                negative_comments=sentiment_results['negative'],
                neutral_comments=sentiment_results['neutral'],
                lecture_content_comments=category_results['講義内容'],
                lecture_materials_comments=category_results['講義資料'],
                operation_comments=category_results['運営'],
                other_comments=category_results['その他'],
                dangerous_comments=dangerous_comments
            )
            
            return self.results
            
        except Exception as e:
            st.error(f"分析中にエラーが発生しました: {e}")
            return None
    
    def _identify_comment_columns(self, df):
        """コメント列を自動識別"""
        # データ型とNULL率から推定
        comment_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':  # 文字列型
                null_ratio = df[col].isnull().mean()
                avg_length = df[col].dropna().astype(str).str.len().mean()
                
                # 平均文字数が20以上、NULL率が50%以下の列をコメント列と判定
                if avg_length > 20 and null_ratio < 0.5:
                    comment_cols.append(col)
        
        return comment_cols