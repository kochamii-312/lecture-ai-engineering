# main.py

import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from preprocess import split_into_sentences
from labeling import get_sentiment_label, get_category_label
from clustering import summarize_comments

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
            
            lecture_content_comment_list = []
            lecture_materials_comment_list = []
            operation_comment_list = []
            others_comment_list = []
            
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
            
            print(f"\n positive_comment_list: {positive_comment_list}, 件数: {len(positive_comment_list)})")
            print(f"\n negative_comment_list: {negative_comment_list}, 件数: {len(negative_comment_list)})")
            
            for col in comment_columns:
                print(f"\nProcessing column: {col}")
                splited_sentences = split_into_sentences(df[col].dropna().tolist())
                for index, comment_text in enumerate(splited_sentences):
                    category = get_category_label(comment_text)
                    print(f"Row {index}: '{comment_text}' -> Category: {category}")
                    if category == '講義内容':
                        lecture_content_comment_list.append(comment_text)
                    elif category == '講義資料':
                        lecture_materials_comment_list.append(comment_text)
                    elif category == '運営':
                        operation_comment_list.append(comment_text)
                    else:
                        others_comment_list.append(comment_text)
            print(f"\n lecture_content_comment_list: {lecture_content_comment_list}, 件数: {len(lecture_content_comment_list)})")
            print(f"\n lecture_materials_comment_list: {lecture_materials_comment_list}, 件数: {len(lecture_materials_comment_list)})")
            print(f"\n operation_comment_list: {operation_comment_list}, 件数: {len(operation_comment_list)})")
            print(f"\n others_comment_list: {others_comment_list}, 件数: {len(others_comment_list)})")
            
            st.write("分析結果:")
            
            # ポジネガの要約
            positive_summary = summarize_comments(positive_comment_list, n_summary=10)
            negative_summary = summarize_comments(negative_comment_list, n_summary=10)

            st.subheader("【ポジティブ要約】")
            for i, comment in enumerate(positive_summary, 1):
                st.write(f"{i}. {comment}")

            st.subheader("【ネガティブ要約】")
            for i, comment in enumerate(negative_summary, 1):
                st.write(f"{i}. {comment}")

            st.write("重要なコメントや危険度の高いコメントを抽出して表示します。")
            # important_comments = df[df['comments'].str.contains('重要|危険', na=False)]
            # st.dataframe(important_comments)
    else:
        st.info("ファイルをアップロードしてください。")

if __name__ == "__main__":
    main()