# main.py
import streamlit as st
import pandas as pd
from classify import classify_comment_list
from preprocess import preprocess_df
from visualize import show_visualizations

st.title("講義アンケートコメント分析ツール（GPT-4o対応）")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'comment' not in df.columns:
        st.error("CSVに 'comment' カラムが必要です。")
        st.stop()

    st.write("アップロードされたデータ：", df.head())

    df = preprocess_df(df)

    if st.button("GPT-4oで分類する"):
        df = classify_comment_list(df)

        st.success("分類完了！")
        st.dataframe(df)

        show_visualizations(df)

        st.download_button("CSV出力", df.to_csv(index=False).encode("utf-8"), file_name="classified_comments.csv")
