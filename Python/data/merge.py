#妙見岳と仁田峠の値を加重平均したデータをファイルに出力

import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# 緯度・経度から距離（km）を計算する関数
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半径（km）
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 各ファイルのパス
input_file1 = "D:/Master/Nakayama/Myoken.txt"
input_file2 = "D:/Master/Nakayama/Nita.txt"
output_file = "D:/Master/Nakayamalab/merge_MyokenandNita.txt"

# 格子点の位置
grid_lat = 32.75000
grid_lon = 130.31250

# 各観測点の緯度・経度
myoken_lat, myoken_lon = 32.75625, 130.28568
nita_lat, nita_lon = 32.75088, 130.28554

# 距離の計算
dist_myoken = haversine(myoken_lat, myoken_lon, grid_lat, grid_lon)
dist_nita = haversine(nita_lat, nita_lon, grid_lat, grid_lon)

# 重み計算（距離の逆数 → 正規化）
w_myoken = 1 / dist_myoken
w_nita = 1 / dist_nita
w_sum = w_myoken + w_nita
weight_myoken = w_myoken / w_sum
weight_nita = w_nita / w_sum

# データの読み込み
df_myoken = pd.read_csv(input_file1, delim_whitespace=True, header=None,
                        names=["YYYY", "MMDD", "HHMM", "value_b", "value_c"])
df_nita = pd.read_csv(input_file2, delim_whitespace=True, header=None,
                      names=["YYYY", "MMDD", "HHMM", "value_b", "value_c"])

# データを時刻で結合（内部的にinner join）
df_merged = pd.merge(df_myoken, df_nita, on=["YYYY", "MMDD", "HHMM"], suffixes=("_myoken", "_nita"))

# 重み付け平均を計算
df_merged["value_b"] = df_merged["value_b_myoken"] * weight_myoken + df_merged["value_b_nita"] * weight_nita
df_merged["value_c"] = df_merged["value_c_myoken"] * weight_myoken + df_merged["value_c_nita"] * weight_nita

# 出力列を整形
output_df = df_merged[["YYYY", "MMDD", "HHMM", "value_b", "value_c"]].copy()

# MMDD と HHMM を 4桁ゼロ埋め（文字列として出力）
output_df["MMDD"] = output_df["MMDD"].astype(str).str.zfill(4)
output_df["HHMM"] = output_df["HHMM"].astype(str).str.zfill(4)

# ファイル出力（空白区切り）
output_df.to_csv(output_file, sep=" ", index=False, header=False)


# 重みを表示（任意）
print(f"妙見岳→格子点の距離: {dist_myoken:.3f} km")
print(f"仁田峠→格子点の距離: {dist_nita:.3f} km")
print(f"重み: 妙見岳 = {weight_myoken:.3f}, 仁田峠 = {weight_nita:.3f}")
