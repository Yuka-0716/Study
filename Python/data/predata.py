#実地観測データをテキストデータ化する。比較するための前段階

import pandas as pd

# 入力ファイルと出力ファイルのパス
input_file = "D:/Master/Nita.xlsx"
output_file = "D:/Master/Nakayamalab/pre_Nita.txt"

# Excelファイルの読み込み（3行目からデータが始まる）
df = pd.read_excel(input_file, skiprows=2, header=None, usecols=[0, 1, 2])

# 列に名前をつける
df.columns = ["datetime", "value_b", "value_c"]

# 日付と時刻の整形：年、月日、時分の列を作成
df["datetime"] = pd.to_datetime(df["datetime"])
df["YYYY"] = df["datetime"].dt.strftime("%Y")
df["MMDD"] = df["datetime"].dt.strftime("%m%d")
df["HHMM"] = df["datetime"].dt.strftime("%H%M")

# 必要な列を順番に並べる
output_df = df[["YYYY", "MMDD", "HHMM", "value_b", "value_c"]]

# 出力ファイルとして保存（区切りはスペース）
output_df.to_csv(output_file, sep=" ", index=False, header=False)
