# main.py
import streamlit as st
import pandas as pd
from preprocess import merge_comment_columns
from visualize import show_all_visualizations

st.title("松尾研講義アンケート分析アプリ")

st.sidebar.header("このアプリのガイド")
st.sidebar.info("講義アンケートのCSVファイルをアップロードすると、重要なコメントや危険度の高いコメントを分析してCSVに出力します。")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ファイルのデータを表示
    bytes_data = uploaded_file.getvalue()
    st.write(f"ファイルサイズ: {len(bytes_data)} bytes")
    
    # CSVの場合はデータフレームとして読み込む
    if uploaded_file.name.endswith('.csv'):
        st.write("CSVデータのプレビュー:")
        st.dataframe(df.head())

    if st.button("GPT-4oで分類・分析する"):

        st.success("分類・分析が完了しました")

        show_all_visualizations()

        # st.download_button(
        #     "分類結果をCSVでダウンロード",
        #     result_df.to_csv(index=False).encode("utf-8"),
        #     file_name="classified_output.csv"
        # )
