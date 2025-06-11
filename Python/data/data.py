#実地観測データを0:10始まり１０分刻みのデータに変換。ここで出力されたデータを比較する。

import pandas as pd
from datetime import datetime, timedelta

# 入出力ファイルパス
input_file = "D:/Master/Nakayama/pre_Nita.txt"
output_file = "D:/Master/Nakayamalab/Nita.txt"

# データの読み込み
df = pd.read_csv(input_file, delim_whitespace=True, header=None,
                 names=["YYYY", "MMDD", "HHMM", "value_b", "value_c"])

# 日付時刻を datetime 形式に変換（ゼロ埋めでエラー回避）
df["datetime"] = pd.to_datetime(
    df["YYYY"].astype(str).str.zfill(4) +
    df["MMDD"].astype(str).str.zfill(4) +
    df["HHMM"].astype(str).str.zfill(4),
    format="%Y%m%d%H%M"
)

# 平均データ格納用
avg_data = []

# 平均を計算（i行目とi+1行目の中間）
for i in range(len(df) - 1):
    time1 = df.loc[i, "datetime"]
    time2 = df.loc[i + 1, "datetime"]
    
    # 時刻差が20分でなければスキップ（10分刻み前提）
    if (time2 - time1).seconds != 600:
        continue
    
    # 中間時刻
    midpoint = time1 + timedelta(minutes=5)
    
    # 値の平均
    avg_b = (df.loc[i, "value_b"] + df.loc[i + 1, "value_b"]) / 2
    avg_c = (df.loc[i, "value_c"] + df.loc[i + 1, "value_c"]) / 2
    
    # 日付部分の取得
    yyyy = midpoint.strftime("%Y")
    mmdd = midpoint.strftime("%m%d")
    hhmm = midpoint.strftime("%H%M")
    
    avg_data.append([yyyy, mmdd, hhmm, avg_b, avg_c])

# DataFrame に変換して保存
avg_df = pd.DataFrame(avg_data, columns=["YYYY", "MMDD", "HHMM", "value_b", "value_c"])
avg_df.to_csv(output_file, sep=" ", index=False, header=False)
