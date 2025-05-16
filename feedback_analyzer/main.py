# main.py
import streamlit as st
import pandas as pd
from classify import analyze_comments
from visualize import show_all_visualizations
from preprocess import merge_comment_columns

st.title("講義アンケートフィードバック分析ツール")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df_long = merge_comment_columns(df)  # 複数列のコメントを1列に統合
    st.write("統合されたコメント数：", len(df_long))

    if st.button("GPT-4oで分類・分析する"):
        result_df, summaries = analyze_comments(df_long)

        st.success("分類・分析が完了しました")

        show_all_visualizations(result_df, summaries)

        st.download_button(
            "分類結果をCSVでダウンロード",
            result_df.to_csv(index=False).encode("utf-8"),
            file_name="classified_output.csv"
        )
