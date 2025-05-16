# preprocess.py
import pandas as pd

def preprocess_text(text: str) -> str:
    text = str(text).replace("\n", " ").strip()
    return text

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df["comment"] = df["comment"].apply(preprocess_text)
    return df
