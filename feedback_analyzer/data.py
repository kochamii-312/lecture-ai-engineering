import pandas as pd
import io

# 変換元のExcelファイルのパス
excel_file = 'data/Day1_アンケート_.xlsx'

# Excelファイルを読み込む
excel_df = pd.read_excel(excel_file, sheet_name=0)
    
# DataFrameをCSV形式に変換（インデックス付き）
csv_buffer_ = io.StringIO()
excel_df.to_csv(csv_buffer_, index=True)
csv_buffer_.seek(0)  # 読み込み位置を先頭に戻す

# 変換したCSVを再度DataFrameとして読み込む
train_df = pd.read_csv(csv_buffer_)