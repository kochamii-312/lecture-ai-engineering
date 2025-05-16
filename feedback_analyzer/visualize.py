# visualize.py
import streamlit as st
import pandas as pd

def show_visualizations(df: pd.DataFrame):
    st.subheader("カテゴリごとの件数")
    st.bar_chart(df["category"].value_counts())

    st.subheader("ポジネガ割合")
    st.bar_chart(df["sentiment"].value_counts())

    st.subheader("重要コメント（スコア>=4）")
    st.dataframe(df[df["importance"] >= 4].sort_values("importance", ascending=False))
