# main.py
import streamlit as st
import pandas as pd
import os as os
from visualize import show_all_visualizations
from preprocess import merge_comment_columns
from lecture_analyzer import LectureAnalyzer
from dotenv import load_dotenv
from typing import List, Tuple
import plotly.express as px
import plotly.graph_objects as go

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def display_results(results):
    """
    分析結果を表示する関数
    
    Args:
        results (AnalysisResults): 分析結果オブジェクト
    """
    st.header("📊 分析結果")
    
    # 概要統計を表示
    display_summary_stats(results)
    
    # 感情分析結果
    st.subheader("😊 感情分析結果")
    display_sentiment_analysis(results)
    
    st.divider()
    
    # カテゴリ分析結果
    st.subheader("📂 カテゴリ分析結果")
    display_category_analysis(results)
    
    st.divider()
    
    # 危険コメント検出結果
    st.subheader("⚠️ 危険コメント検出結果")
    display_dangerous_comments(results)

def display_summary_stats(results):
    """概要統計の表示"""
    total_comments = (
        len(results.positive_comments) + 
        len(results.negative_comments) + 
        len(results.neutral_comments)
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("総コメント数", total_comments)
    
    with col2:
        st.metric("ポジティブ", len(results.positive_comments))
    
    with col3:
        st.metric("ネガティブ", len(results.negative_comments))
    
    with col4:
        st.metric("危険コメント", len(results.dangerous_comments))

def display_sentiment_analysis(results):
    """感情分析結果の表示"""
    # 感情分布の円グラフ
    sentiment_counts = {
        "ポジティブ": len(results.positive_comments),
        "ネガティブ": len(results.negative_comments),
        "ニュートラル": len(results.neutral_comments)
    }
    
    # Plotlyで円グラフ作成
    fig = px.pie(
        values=list(sentiment_counts.values()),
        names=list(sentiment_counts.keys()),
        title="感情分布",
        color_discrete_map={
            "ポジティブ": "#28a745",
            "ネガティブ": "#dc3545", 
            "ニュートラル": "#6c757d"
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 詳細表示用のタブ
    tab1, tab2, tab3 = st.tabs(["👍 ポジティブ", "👎 ネガティブ", "😐 ニュートラル"])
    
    with tab1:
        display_comment_list("ポジティブコメント", results.positive_comments, "success")
    
    with tab2:
        display_comment_list("ネガティブコメント", results.negative_comments, "error")
    
    with tab3:
        display_comment_list("ニュートラルコメント", results.neutral_comments, "info")

def display_category_analysis(results):
    """カテゴリ分析結果の表示"""
    category_counts = {
        "講義内容": len(results.lecture_content_comments),
        "講義資料": len(results.lecture_materials_comments),
        "運営": len(results.operation_comments),
        "その他": len(results.other_comments)
    }
    
    # 棒グラフで表示
    fig = px.bar(
        x=list(category_counts.keys()),
        y=list(category_counts.values()),
        title="カテゴリ別コメント数",
        labels={"x": "カテゴリ", "y": "コメント数"},
        color=list(category_counts.values()),
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # カテゴリ別詳細表示
    tab1, tab2, tab3, tab4 = st.tabs(["📚 講義内容", "📄 講義資料", "⚙️ 運営", "📝 その他"])
    
    with tab1:
        display_comment_list("講義内容に関するコメント", results.lecture_content_comments)
    
    with tab2:
        display_comment_list("講義資料に関するコメント", results.lecture_materials_comments)
    
    with tab3:
        display_comment_list("運営に関するコメント", results.operation_comments)
    
    with tab4:
        display_comment_list("その他のコメント", results.other_comments)

def display_dangerous_comments(results):
    """危険コメントの表示"""
    if len(results.dangerous_comments) == 0:
        st.success("✅ 危険なコメントは検出されませんでした。")
        return
    
    st.warning(f"⚠️ {len(results.dangerous_comments)}件の危険な可能性のあるコメントが検出されました。")
    
    for i, (comment, score) in enumerate(results.dangerous_comments, 1):
        with st.expander(f"危険コメント #{i} (スコア: {score:.2f})"):
            st.text(comment)
            
            # 危険度に応じて色分け
            if score > 0.9:
                st.error("⚠️ 高リスク")
            elif score > 0.8:
                st.warning("⚠️ 中リスク")
            else:
                st.info("⚠️ 低リスク")

def display_comment_list(title, comments, message_type="info"):
    """コメントリストの表示"""
    if not comments:
        st.info("該当するコメントはありません。")
        return
    
    st.write(f"**{title}** ({len(comments)}件)")
    
    # ページネーション対応
    items_per_page = 10
    total_pages = (len(comments) + items_per_page - 1) // items_per_page
    
    if total_pages > 1:
        page = st.selectbox(
            "ページを選択", 
            range(1, total_pages + 1), 
            key=f"page_{title}"
        )
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(comments))
        display_comments = comments[start_idx:end_idx]
    else:
        display_comments = comments[:items_per_page]
    
    for i, comment in enumerate(display_comments, 1):
        if message_type == "success":
            st.success(f"{i}. {comment}")
        elif message_type == "error":
            st.error(f"{i}. {comment}")
        elif message_type == "warning":
            st.warning(f"{i}. {comment}")
        else:
            st.info(f"{i}. {comment}")

def display_cluster_results(comments, title, embedder=None):
    """
    クラスタリング結果の表示（既存のcluster_and_rank機能を活用）
    
    Args:
        comments: コメントリスト
        title: 表示タイトル
        embedder: CommentEmbedder インスタンス（オプション）
    """
    if not comments or len(comments) < 3:
        st.info(f"{title}: クラスタリングに十分なコメントがありません。")
        return
    
    st.subheader(f"🔍 {title} - クラスタ分析")
    
    if embedder is None:
        # 簡単な頻出語分析で代替
        display_word_frequency(comments, title)
        return
    
    try:
        # クラスタリング実行
        cluster_results = embedder.cluster_and_rank(comments, n_clusters=min(5, len(comments)//2))
        
        for i, (count, representative) in enumerate(cluster_results, 1):
            with st.expander(f"クラスタ {i}: {count}件"):
                st.write(f"**代表コメント:** {representative}")
                
                # プログレスバーで件数を視覚化
                st.progress(count / len(comments))
                
    except Exception as e:
        st.error(f"クラスタリング中にエラーが発生しました: {e}")
        display_word_frequency(comments, title)

def display_word_frequency(comments, title):
    """簡単な頻出語分析"""
    from collections import Counter
    import re
    
    # 簡単な日本語トークン化（本格的にはMeCabなどを使用）
    all_words = []
    for comment in comments:
        # ひらがな、カタカナ、漢字を抽出
        words = re.findall(r'[ひらがなカタカナ漢字]+', comment)
        all_words.extend([w for w in words if len(w) > 1])
    
    word_freq = Counter(all_words)
    top_words = word_freq.most_common(10)
    
    if top_words:
        st.write(f"**{title} - 頻出語TOP10**")
        for word, count in top_words:
            st.write(f"- {word}: {count}回")

def main():
    st.title("📊 松尾研講義アンケート分析アプリ")
    
    uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ ファイル読み込み完了 ({len(df)}行)")
            
            # データプレビュー
            with st.expander("データプレビュー"):
                st.dataframe(df.head())
            
            if st.button("🚀 分析開始"):
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 分析実行
                analyzer = LectureAnalyzer(HF_TOKEN)
                
                progress_bar.progress(20)
                status_text.text("モデル初期化中...")
                
                results = analyzer.analyze(df)
                
                progress_bar.progress(100)
                status_text.text("分析完了!")
                
                if results:
                    # 結果表示
                    display_results(results)
                    
                    # CSV出力
                    csv_file = results.export_csv()
                    with open(csv_file, 'rb') as f:
                        st.download_button(
                            "📥 結果をCSVダウンロード",
                            f.read(),
                            file_name=csv_file,
                            mime="text/csv"
                        )
                
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {e}")
    
