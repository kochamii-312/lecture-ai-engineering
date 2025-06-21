# preprocess.py
import pandas as pd
import re

def split_into_sentences(comment_list):
    """
    各要素に複数文含むリストを受け取り、文単位で分割して新しいリストを返す関数
    Parameters:
        comment_list (list of str): 元のコメントリスト（各要素に複数文が含まれることがある）
    Returns:
        list of str: すべての文を1文ずつ展開した新しいリスト
    """
    sentence_list = []
    for comment in comment_list:
        if not isinstance(comment, str):  # ← 安全チェック追加
            continue
        # 「。」や「！」改行などで分割（必要に応じて追加）
        sentences = re.split(r'(?:[。．！？!?]+(?:\\n|\n)?|\\n)', comment)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:  # 空文字は除外
                sentence_list.append(sentence)
    print("sentence_list: ", sentence_list)
    print("sentence_listの件数: ", len(sentence_list))
    return sentence_list

def merge_comment_columns(df, columns, sep=" ", empty_value=""):
    """
    複数のカラムを1つのリストにまとめる関数
    
    Parameters:
        df (pd.DataFrame): 元のデータフレーム
        columns (List[Union[int, str]]): 結合対象のカラム番号またはカラム名のリスト
        sep (str): 各カラム間の区切り文字（デフォルトは空白）
        empty_value (str): 値が存在しない行の場合の戻り値（デフォルトは空文字）

    Returns:
        List[str]: 各行を結合した文字列のリスト
        
    Raises:
        ValueError: 指定されたカラムが存在しない場合
        TypeError: 引数の型が不正な場合
    """
    # 入力検証
    if not isinstance(df, pd.DataFrame):
        raise TypeError("dfはpandas.DataFrameである必要があります")
    
    if not isinstance(columns, list) or not columns:
        raise ValueError("columnsは空でないリストである必要があります")
    
    if not isinstance(sep, str):
        raise TypeError("sepは文字列である必要があります")
    
    # カラム名/番号の正規化と存在確認
    normalized_columns = []
    for col in columns:
        if isinstance(col, int):
            if col < 0 or col >= len(df.columns):
                raise ValueError(f"カラム番号 {col} は範囲外です（0-{len(df.columns)-1}）")
            normalized_columns.append(df.columns[col])
        elif isinstance(col, str):
            if col not in df.columns:
                raise ValueError(f"カラム '{col}' が存在しません")
            normalized_columns.append(col)
        else:
            raise TypeError(f"カラム指定は整数または文字列である必要があります: {col}")
    
    # ベクトル化された処理で高速化
    def merge_row_values(row):
        values = []
        for col in normalized_columns:
            if pd.notna(row[col]) and str(row[col]).strip():
                values.append(str(row[col]).strip())
        return sep.join(values) if values else empty_value
    
    return df[normalized_columns].apply(merge_row_values, axis=1).tolist()


    # # 行ごとに処理
    # for index, row in df.iterrows():
    #     values = []
    #     for col in column_names:
    #         if col in row and pd.notna(row[col]):
    #             values.append(str(row[col]).strip())
    #     if values:
    #         merged_list.append(sep.join(values))
    
