import pandas as pd

# 変換元のExcelファイルのパス
excel_file = 'data/Day1_アンケート_.xlsx'

# 読み込むシート名
train_excel = pd.read_excel(excel_file, sheet_name=0)

# 保存先のCSVファイルのパス
train_df = 'Day1_アンケート.csv'

# CSVとして保存（インデックスは不要な場合はFalseに）
train_excel.to_csv(train_df)