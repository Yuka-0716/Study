import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import mode

# ディレクトリパス
data_dir = "E:/Master/FogData(5)"

# テキストファイルの取得
files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".txt")]

# 描画する列
target_columns = ["CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE"]

# 各ファイルの処理
for input_file in files:
    print(f"Processing file: {input_file}")

    # データの読み込み
    data = pd.read_csv(input_file, sep="\t", header=None, 
                       names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"], na_values="N/A")

    # 時間の統合
    data["Timestamp"] = pd.to_datetime(data["days"].astype(str) + data["Hour"].astype(str).str.zfill(4), format="%Y%m%d%H%M")

    # 各列の統計量を計算して出力
    for column in target_columns:
        column_data = data[column].dropna()
        total_count = column_data.count()
        mean_value = column_data.mean()
        median_value = column_data.median()

        # 最頻値の計算
        mode_result = mode(column_data, nan_policy='omit')
        if isinstance(mode_result.count, np.ndarray) and mode_result.count.size > 0:
            mode_value = mode_result.mode[0]
        else:
            mode_value = None

        print(f"\n=== {column} ({input_file}) ===")
        print(f"Total data points: {total_count}")
        print(f"Mean: {mean_value:.2f}")
        print(f"Median: {median_value:.2f}")
        print(f"Mode: {mode_value}")
