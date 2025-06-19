# visualize.py
import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from data import train_df
from preprocess import split_into_sentences, merge_comment_columns
from sentiment_classify import SentimentClassifier
from category_classify import CategoryClassifier
from clustering import CommentEmbedder
from dotenv import load_dotenv
from comment_lists import positive_comment_list, negative_comment_list, neutral_comment_list, lecture_content_comment_list, lecture_materials_comment_list, operation_comment_list, others_comment_list

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# メモ：講義回ごとに分ける
# メモ：CSVファイルで出力できるようにする
def show_all_visualizations():
    st.header("分析結果")
    st.subheader("感情分析")
    show_setiment_visulization()
    st.divider()
    st.subheader("カテゴリ別")
    show_category_visualization()
    st.divider()
    show_dangerous_comment_visualization()

def show_setiment_visulization():
    """
    「特に良かった部分」の欄のコメントと、テキスト分類器の結果をpositive_comment_listに格納、
    「分かりにくかった点や不満があった点」の欄のコメントと、テキスト分類器の結果をnegative_comment_listに格納する
    それぞれのlistをクラスタリングして要約
    """
    from main import df
    positive_comment_list.append(split_into_sentences(df[-5]))
    negative_comment_list.append(split_into_sentences(df[-4]))

    columns = ['comment3_about_teacher', 'comment4_future_suggestions', 'comment5_free']
    train_comment_list = split_into_sentences(merge_comment_columns(train_df, columns))
    comment_list = split_into_sentences(merge_comment_columns(df, columns))
    
    sc = SentimentClassifier()
    sc.train_on(train_comment_list)
    sc.predict_on(comment_list)

    # クラスタリング
    embedder = CommentEmbedder(hf_token=HF_TOKEN)

    # クラスタを結合して要約
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ポジティブコメントの要約")
        clusters = embedder.cluster_comments(positive_comment_list, n_clusters=5)
        # メモ: LLMを使わず代表コメントでも
        for cluster_id, items in clusters.items():
            summary = embedder.summarize_cluster(items)
            st.text(f"- クラスタ {cluster_id}. {summary}")
    with col2:
        st.subheader("ネガティブコメントの要約")
        clusters = embedder.cluster_comments(negative_comment_list, n_clusters=5)
        # メモ: LLMを使わず代表コメントでも
        for cluster_id, items in clusters.items():
            summary = embedder.summarize_cluster(items)
            st.text(f"- クラスタ {cluster_id}. {summary}")
    st.divider()

def show_category_visualization():
    columns = ['comment1_positive, comment2_negative, commet3_about_teacher, comment4_future_suggestions, comment5_free']
    train_comment_list = split_into_sentences(merge_comment_columns(train_df, columns))
    cc = CategoryClassifier()
    cc.train_on(train_comment_list)
    cc.predict_on(positive_comment_list)
    cc.predict_on(negative_comment_list)

    # カテゴリごとの割合
    comment_lists = [
        lecture_content_comment_list,
        lecture_materials_comment_list,
        operation_comment_list,
        others_comment_list
    ]
    category_names = ["講義内容", "講義資料", "運営", "その他"]
    counts = [len(lst) for lst in comment_lists]

    # Streamlit 表示
    st.subheader("📊コメントカテゴリの円グラフ可視化")

    # 円グラフ作成
    fig, ax = plt.subplots()
    ax.pie(counts, labels=category_names, autopct='%1.1f%%', startangle=90, counterclock=False)
    ax.axis('equal')  # 円を正円に

    st.pyplot(fig)

    # 件数のテーブル
    st.markdown("### 📋件数データ")
    for name, count in zip(category_names, counts):
        st.write(f"- {name}: {count}件")

    # 重要度スコアが高い上位10件
    st.subheader("🔝カテゴリ別重要度の高いコメント")
    st.text("カテゴリ別に重要度が高いコメントを10件ランキング表示しています。")
    embedder = CommentEmbedder(hf_token=HF_TOKEN)
    tab1, tab2, tab3, tab4 = st.tabs("講義内容", "講義資料", "運営", "その他")
    with tab1:
        st.markdown("### 📊カテゴリ「講義内容」重要度ランキング")
        for i, (count, representative) in enumerate(embedder.cluster_and_rank(lecture_content_comment_list), 1):
            st.markdown(f"**{i}. 件数: {count}件**")
            st.write(f"代表コメント: {representative}")
    with tab2:
        st.markdown("### 📊カテゴリ「講義資料」重要度ランキング")
        for i, (count, representative) in enumerate(embedder.cluster_and_rank(lecture_materials_comment_list), 1):
            st.markdown(f"**{i}. 件数: {count}件**")
            st.write(f"代表コメント: {representative}")
    with tab3:
        st.markdown("### 📊カテゴリ「運営」重要度ランキング")
        for i, (count, representative) in enumerate(embedder.cluster_and_rank(operation_comment_list), 1):
            st.markdown(f"**{i}. 件数: {count}件**")
            st.write(f"代表コメント: {representative}")
    with tab4:
        st.markdown("### 📊カテゴリ「その他」重要度ランキング")
        for i, (count, representative) in enumerate(embedder.cluster_and_rank(others_comment_list), 1):
            st.markdown(f"**{i}. 件数: {count}件**")
            st.write(f"代表コメント: {representative}")

def show_dangerous_comment_visualization():
    from main import df
    columns = ['comment1_positive, comment2_negative, commet3_about_teacher, comment4_future_suggestions, comment5_free']
    flagged_comments = detect_dangerous_comments(split_into_sentences(merge_comment_columns(df, columns)))
    if flagged_comments != 0:
        st.text(f"⚠️ 危険コメント {len(flagged_comments)} 件検出:")
        for comment, score in flagged_comments:
            st.text(f"- {comment} (score:{score:.2f})")
    else:
        st.text("✅ 危険コメントは検出されませんでした。")

def detect_dangerous_comments(texts, threshold=0.8):
    api_url = "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli"
    label_danger = "危険または不適切"

    flagged = []
    for text in texts:
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": [label_danger, "安全"], "multi_label": False}
        }
        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()
        if result["labels"][0] == label_danger and result["scores"][0] > threshold:
            flagged.append((text, result["scores"][0]))
    if not flagged:
        return 0
    return flagged
