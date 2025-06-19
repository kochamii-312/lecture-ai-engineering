import pandas as pd

# 変換元のExcelファイルのパス
excel_file = 'data/Day1_アンケート.xlsx'

# 読み込むシート名（通常は1つ目のシート）
df = pd.read_excel(excel_file, sheet_name=0)

# 保存先のCSVファイルのパス
csv_file = 'csvsDay1_アンケート.csv'

# CSVとして保存（インデックスは不要な場合はFalseに）
df.to_csv(csv_file, index=False)