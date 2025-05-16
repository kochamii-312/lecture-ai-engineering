# preprocess.py
import pandas as pd

def merge_comment_columns(df):
    comment_columns = [
        "特に良かった点",
        "わかりにくかった部分や改善点",
        "講師についてよかった点や不満があった点",
        "今後開講してほしい講義・分野など",
        "自由に意見"
    ]
    all_comments = []

    for _, row in df.iterrows():
        for col in comment_columns:
            text = str(row.get(col, "")).strip()
            if text:
                all_comments.append({
                    "original_column": col,
                    "comment": text
                })

    return pd.DataFrame(all_comments)
