# main.py

import matplotlib.font_manager
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import japanize_matplotlib
from dotenv import load_dotenv
from preprocess import split_into_sentences
from labeling import get_sentiment_label, get_category_label
from clustering import summarize_comments, cluster_comments
from importance import score_specificity, score_urgency, score_commonality, score_importance, get_cluster_number, get_cluster_size_and_total
from danger import extract_dangerous_comments

# matplotlib.font_manager._rebuild()
# matplotlib.rcParams['font.family'] = 'IPAexGothic'

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def main():

    st.title("📊 講義アンケート分析アプリ")

    tab1, tab2, tab3, tab4 = st.tabs(["📄 アップロードと分析", "😊 センチメント分類", "📈 カテゴリ分類", "🚨 重要度スコア"])
    with tab1:
        st.sidebar.header("ℹ️ このアプリのガイド")
        st.sidebar.info("講義アンケートのexcelファイルをアップロードすると、重要なコメントや危険度の高いコメントを分析します。")

        pos_limit = st.slider("表示するポジティブコメント数", 1, 20, 10)
        neg_limit = st.slider("表示するネガティブコメント数", 1, 20, 10)
        cat_limit = st.slider("カテゴリごとの表示数", 1, 20, 10)
        
        uploaded_file = st.file_uploader("excelファイルをアップロードしてください", type=["xlsx", "xls"], key="excel_upload") # key引数で明示的に識別子を指定
        if uploaded_file:
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file)    
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                st.error("❌ サポートされていないファイル形式です。ExcelまたはCSVファイルをアップロードしてください。")
            
            st.write("👀 プレビュー:")
            st.dataframe(df.head())
            
            # カラム名の変更
            current_columns = df.columns.tolist()
            new_column_names_part = ['comment1_positive', 'comment2_negative', 'comment3_about_teacher', 'comment4_future_suggestions', 'comment5_free']
            current_columns[16:21] = new_column_names_part
            df.columns = current_columns

            if st.button("🚀 分析する"):
                progress = st.progress(0, text="分析を開始しています...")
                positive_comment_list = []
                negative_comment_list = []
                
                lecture_content_comment_list = []
                lecture_materials_comment_list = []
                operation_comment_list = []
                others_comment_list = []
                comment_columns_all = new_column_names_part
                
                progress.progress(10, "コメントを分割・感情分析中...")
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
                
                # カテゴリ分類
                progress.progress(30, "カテゴリ分類中...")
                for col in comment_columns_all:
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
                
                # 重要スコア
                progress.progress(60, "重要度スコア計算中...")
                scored_comments_all = []

                for col in comment_columns_all:
                    comments = df[col].dropna().tolist()
                    splited_sentences = split_into_sentences(comments)
                    clustered = cluster_comments(splited_sentences)
                    for index, comment_text in enumerate(splited_sentences):
                        spec = score_specificity(comment_text)
                        urg = score_urgency(comment_text)
                        cluster_number = get_cluster_number(comment_text, clustered)
                        cluster_size, total_comments = get_cluster_size_and_total(cluster_number, clustered)
                        comm = score_commonality(cluster_size, total_comments)
                        importance_score = score_importance(spec, urg, comm)

                        print(f"Row {index}: '{comment_text}' -> Specificity: {spec}, Urgency: {urg}, Commonality: {comm}, Importance Score: {importance_score}")

                        # 辞書形式でまとめてリストに追加
                        scored_comments_all.append({
                            "comment": comment_text,
                            "specificity": spec,
                            "urgency": urg,
                            "commonality": comm,
                            "importance_score": importance_score,
                            "cluster": cluster_number
                        })

                progress.progress(90, "危険コメントを抽出中...")
                all_comments = sum([split_into_sentences(df[col].dropna().tolist()) for col in comment_columns_all], [])
                dangerous_comments = extract_dangerous_comments(all_comments)

                progress.progress(100, "分析完了！")
                st.success("🎉 分析が完了しました。各タブを確認してください。")
                st.balloons()

                # 分析結果をセッションに保存
                st.session_state.update({
                    'positive_summary': summarize_comments(positive_comment_list, pos_limit),
                    'negative_summary': summarize_comments(negative_comment_list, neg_limit),
                    'lecture_content_summary': summarize_comments(lecture_content_comment_list, cat_limit),
                    'lecture_materials_summary': summarize_comments(lecture_materials_comment_list, cat_limit),
                    'operation_summary': summarize_comments(operation_comment_list, cat_limit),
                    'others_summary': summarize_comments(others_comment_list, cat_limit),
                    'scored_comments_df': pd.DataFrame(scored_comments_all).sort_values(by='importance_score', ascending=False),
                    'dangerous_comments': dangerous_comments,
                    'sentiment_counts': {
                        'ポジティブ': len(positive_comment_list),
                        'ネガティブ': len(negative_comment_list)
                    },
                    'category_counts': {
                        '講義内容': len(lecture_content_comment_list),
                        '講義資料': len(lecture_materials_comment_list),
                        '運営': len(operation_comment_list),
                        'その他': len(others_comment_list)
                    }
                })

            
    if 'positive_summary' in st.session_state:
        with tab2:
            # ポジネガの要約
            st.subheader("✅ ポジティブコメント要約")
            for i, comment in enumerate(st.session_state['positive_summary'], 1):
                st.write(f"{i}. {comment}")

            st.subheader("⚠️ ネガティブコメント要約")
            for i, comment in enumerate(st.session_state['negative_summary'], 1):
                st.write(f"{i}. {comment}")

            st.subheader("📊 感情分布（円グラフ）")
            fig, ax = plt.subplots()
            labels = list(st.session_state['sentiment_counts'].keys())
            sizes = list(st.session_state['sentiment_counts'].values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        with tab3:
            # カテゴリごとの要約
            st.subheader("📘 講義内容に関するコメント")
            for i, comment in enumerate(st.session_state['lecture_content_summary'], 1):
                st.write(f"{i}. {comment}")
            st.subheader("📗 講義資料に関するコメント")
            for i, comment in enumerate(st.session_state['lecture_materials_summary'], 1):
                st.write(f"{i}. {comment}")
            st.subheader("📙 運営に関するコメント")
            for i, comment in enumerate(st.session_state['operation_summary'], 1):
                st.write(f"{i}. {comment}")

            st.subheader("📊 カテゴリ分布（円グラフ）")
            fig2, ax2 = plt.subplots()
            labels = list(st.session_state['category_counts'].keys())
            sizes = list(st.session_state['category_counts'].values())
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')
            st.pyplot(fig2)

        with tab4:
            #重要度スコア上位10件
            st.subheader("🏆 重要度スコア上位コメント")
            top_10 = st.session_state['scored_comments_df'].head(10)
            for _, row in top_10.iterrows():
                category = get_category_label(row['comment'])
                with st.expander(row['comment'][:40] + "..."):
                    st.write(f"コメント全文: {row['comment']}")
                    st.markdown(f"- カテゴリ: **{category}**")
                    st.markdown(f"- 具体性: {row['specificity']} / 1.0")
                    st.markdown(f"- 緊急性: {row['urgency']} / 1.0")
                    st.markdown(f"- 共通性: {row['commonality']:.2f} / 1.0")
                    st.markdown("""
                    <style>
                    .big-font {
                        font-size:20px ！important;
                        font-weight: bold;
                        color: #0066cc;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    st.markdown(f'<p class="big-font">- 重要度スコア: {row['importance_score']} / 10</p>', unsafe_allow_html=True)
                    
            st.subheader("📈 重要度スコア分布")
            fig3, ax3 = plt.subplots()
            st.session_state['scored_comments_df']['importance_score'].hist(bins=20, ax=ax3)
            ax3.set_xlabel("重要度スコア")
            ax3.set_ylabel("件数")
            st.pyplot(fig3)
            
            # 危険コメントの抽出
            st.subheader("🚨 危険コメント")
            if st.session_state['dangerous_comments']:
                for i, comment in enumerate(st.session_state['dangerous_comments'], 1):
                    st.write(f"{i}. {comment}")
            else:
                st.info("危険コメントは見つかりませんでした。")

if __name__ == "__main__":
    main()