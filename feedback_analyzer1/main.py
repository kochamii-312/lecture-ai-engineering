# main.py

import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from preprocess import split_into_sentences
from labeling import get_sentiment_label
from clustering import Clustering

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def main():

    st.title("松尾研講義アンケート分析アプリ")

    st.sidebar.header("このアプリのガイド")
    st.sidebar.info("講義アンケートのexcelファイルをアップロードすると、重要なコメントや危険度の高いコメントを分析します。")

    uploaded_file = st.file_uploader("excelファイルをアップロードしてください", type=["xlsx", "xls"], key="excel_upload") # key引数で明示的に識別子を指定
    if uploaded_file:
        if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file)    
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("サポートされていないファイル形式です。ExcelまたはCSVファイルをアップロードしてください。")
        
        st.write("プレビュー:")
        st.dataframe(df.head())
        
        # カラム名の変更
        current_columns = df.columns.tolist()
        new_column_names_part = ['comment1_positive', 'comment2_negative', 'comment3_about_teacher', 'comment4_future_suggestions', 'comment5_free']
        current_columns[16:21] = new_column_names_part
        df.columns = current_columns

        if st.button("分析する"):
            st.write("分析中...")

            positive_comment_list = []
            negative_comment_list = []
            # 'comment1_positive'カラムから要素を取得し、positive_comment_listに追加
            if 'comment1_positive' in df.columns:
                positive_comments_from_df = df['comment1_positive'].tolist()
                positive_comment_list.extend(split_into_sentences(positive_comments_from_df))
                print("\n positive_comment_list:")
                print(positive_comment_list)
            else:
                print("\n'comment1_positive' column not found in the DataFrame.")
            # 'comment2_negative'カラムから要素を取得し、negative_comment_listに追加
            if 'comment2_negative' in df.columns:
                negative_comments_from_df = df['comment2_negative'].tolist()
                positive_comment_list.extend(split_into_sentences(negative_comments_from_df))
                print("\n negative_comment_list:")
                print(negative_comment_list)
            else:
                print("\n'comment2_negative' column not found in the DataFrame.")
            
            # 残りのカラムの感情分類
            comment_columns = ['comment3_about_teacher', 'comment4_future_suggestions', 'comment5_free']
            for col in comment_columns:
                print(f"\nProcessing column: {col}")
                splited_sentences = split_into_sentences(df[col].dropna().tolist())
                for index, comment_text in enumerate(splited_sentences):
                    sentiment = get_sentiment_label(comment_text)
                    print(f"Row {index}: '{comment_text}' -> Sentiment: {sentiment}")
                    if sentiment == 'positive':
                        positive_comment_list.append(comment_text)
                    elif sentiment == 'negative':
                        negative_comment_list.append(comment_text)
                    
            st.write("分析結果:")
            # # クラスタリング
            # embedder = Clustering(hf_token=HF_TOKEN)

            # # クラスタを結合して要約
            # col1, col2 = st.columns(2)
            # with col1:
            #     st.subheader("ポジティブコメントの要約")
            #     clusters = embedder.cluster_comments(positive_comment_list, n_clusters=5)
            #     # メモ: LLMを使わず代表コメントでも
            #     for cluster_id, items in clusters.items():
            #         summary = embedder.summarize_cluster(items)
            #         st.text(f"- クラスタ {cluster_id}. {summary}")
            # with col2:
            #     st.subheader("ネガティブコメントの要約")
            #     clusters = embedder.cluster_comments(negative_comment_list, n_clusters=5)
            #     # メモ: LLMを使わず代表コメントでも
            #     for cluster_id, items in clusters.items():
            #         summary = embedder.summarize_cluster(items)
            #         st.text(f"- クラスタ {cluster_id}. {summary}")
            # st.divider()

            st.write("重要なコメントや危険度の高いコメントを抽出して表示します。")
            # important_comments = df[df['comments'].str.contains('重要|危険', na=False)]
            # st.dataframe(important_comments)
    else:
        st.info("ファイルをアップロードしてください。")

if __name__ == "__main__":
    main()