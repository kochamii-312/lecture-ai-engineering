# visualize.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_all_visualizations(df: pd.DataFrame, summaries: dict):
    st.header("コメント分類結果の可視化")

    # ポジティブ・ネガティブの要約
    st.subheader("ポジティブコメントの要約")
    st.text(summaries.get("positive_summary", "なし"))

    st.subheader("ネガティブコメントの要約")
    st.text(summaries.get("negative_summary", "なし"))

    # カテゴリごとの割合
    st.subheader("カテゴリごとの件数と割合")
    cat_counts = df["category"].value_counts(normalize=True) * 100
    fig, ax = plt.subplots()
    sns.barplot(x=cat_counts.index, y=cat_counts.values, ax=ax)
    ax.set_ylabel("割合 (%)")
    st.pyplot(fig)

    # 重要度スコアが高い上位10件（カテゴリ別）
    st.subheader("カテゴリ別・重要度上位コメント（上位10件）")
    for category in df["category"].unique():
        st.markdown(f"#### {category}")
        top_comments = df[df["category"] == category].sort_values("importance_score", ascending=False).head(10)
        for i, row in top_comments.iterrows():
            st.markdown(f"- ({row['importance_score']:.2f}) {row['comment']}")

    # 危険度スコア0.9以上のコメント
    st.subheader("危険コメント（danger_score >= 0.9）")
    danger_comments = df[df["danger_score"] >= 0.9]
    for i, row in danger_comments.iterrows():
        st.markdown(f"- ({row['danger_score']:.2f}) {row['comment']}")