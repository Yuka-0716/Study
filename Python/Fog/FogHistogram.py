#雲特性プロダクトの各変数についてヒストグラムを作成し表示させる。平均値・中央値・最頻値、各変数のデータ数とヒストグラムの値も出力。

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ファイルパス
input_file = "D:/Master/FogData/FogData(12)/202403-fog.txt"

# データの読み込み
data = pd.read_csv(input_file, sep="\t", header=None, 
                   names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"], na_values="N/A")

# 時間の統合
data["Timestamp"] = pd.to_datetime(data["days"].astype(str) + data["Hour"].astype(str).str.zfill(4),
                                   format="%Y%m%d%H%M")

# 描画対象列とビン設定
target_columns_bins = {
    "CLOT": (0, 21, 1.0),
    "CLTT": (230, 300, 10.0),
    "CLTH": (0, 5.0, 0.5),
    "CLER_23": (0, 30, 5.0),
    "CTYPE": (0, 10, 1.0)
}

# 各変数ごとにヒストグラムと統計情報の出力
for column, (start, end, step) in target_columns_bins.items():
    plt.figure(figsize=(10, 6))

    bins = np.arange(start, end + step, step)
    col_data = data[column].dropna()

    # ヒストグラムの描画
    n, bins, patches = plt.hist(col_data, bins=bins, alpha=0.7, label=column, edgecolor='black')

    # 統計量の計算
    mean_val = col_data.mean()
    median_val = col_data.median()
    mode_val = col_data.mode().iloc[0] if not col_data.mode().empty else np.nan

    # グラフ設定
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Sample Count")
    plt.grid(True)
    plt.tight_layout()

    # 情報出力
    print(f"\n=== {column} ===")
    print(f"Total data points: {col_data.count()}")
    print(f"Mean:   {mean_val:.3f}")
    print(f"Median: {median_val:.3f}")
    print(f"Mode:   {mode_val:.3f}")
    print(f"Histogram values: {n}")
    print(f"Bin edges: {bins}")

    plt.show()
