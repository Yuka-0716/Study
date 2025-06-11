import os
import pandas as pd
import numpy as np

# ファイルパス
cloud_dir = "E:/Master/rawdata/202203_data.txt"

# ファイルの確認
cloud_files = [cloud_dir] if os.path.isfile(cloud_dir) else [os.path.join(cloud_dir, f) for f in os.listdir(cloud_dir) if f.endswith('.txt')]

# ビンの設定
clot_bins = np.arange(0, 351, 50)  # 0から300まで50区切り
cltt_bins = np.arange(230, 331, 10)  # 230から330まで10区切り
clth_bins = np.linspace(0, 10, 11)  # 0から10まで10区切り
cler_bins = np.arange(0, 101, 10)  # 0から100まで10区切り
ctype_bins = np.linspace(0, 10, 11)  # 0から10まで1区切り（11区切り）

# データ格納用（初期化）
clot_counts = pd.Series(0, index=pd.IntervalIndex.from_breaks(clot_bins, closed='left'))
cltt_counts = pd.Series(0, index=pd.IntervalIndex.from_breaks(cltt_bins, closed='left'))
clth_counts = pd.Series(0, index=pd.IntervalIndex.from_breaks(clth_bins, closed='left'))
cler_counts = pd.Series(0, index=pd.IntervalIndex.from_breaks(cler_bins, closed='left'))
ctype_counts = pd.Series(0, index=pd.IntervalIndex.from_breaks(ctype_bins, closed='left'))

# N/Aカウント用
na_counts = {"CLOT": 0, "CLTT": 0, "CLTH": 0, "CLER_23": 0, "CTYPE": 0}

# データを読み込む
for cloud_file in cloud_files:
    cloud_data = pd.read_csv(
        cloud_file, 
        delim_whitespace=True, 
        header=None, 
        names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"],
        usecols=[0, 1, 2, 3, 4, 5, 6]
    )

    # 各列のN/Aカウント
    for column in ["CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE"]:
        na_counts[column] += cloud_data[column].isna().sum()

    # 各列ごとにビン分類とカウント
    clot_counts += pd.cut(cloud_data["CLOT"].dropna(), bins=clot_bins, right=False).value_counts().reindex(clot_counts.index, fill_value=0)
    cltt_counts += pd.cut(cloud_data["CLTT"].dropna(), bins=cltt_bins, right=False).value_counts().reindex(cltt_counts.index, fill_value=0)
    clth_counts += pd.cut(cloud_data["CLTH"].dropna(), bins=clth_bins, right=False).value_counts().reindex(clth_counts.index, fill_value=0)
    cler_counts += pd.cut(cloud_data["CLER_23"].dropna(), bins=cler_bins, right=False).value_counts().reindex(cler_counts.index, fill_value=0)
    ctype_counts += pd.cut(cloud_data["CTYPE"].dropna(), bins=ctype_bins, right=False).value_counts().reindex(ctype_counts.index, fill_value=0)

# 結果の表示
print("CLOT counts (0-300, 50 bin):")
print(clot_counts)
print("\nCLTT counts (230-330, 10 bins):")
print(cltt_counts)
print("\nCLTH counts (0-10, 10 bins):")
print(clth_counts)
print("\nCLER_23 counts (0-100, 10 bin):")
print(cler_counts)
print("\nCTYPE counts (0-10, 1 bin, 11 bins):")
print(ctype_counts)

# N/Aの数を表示
print("\nN/A counts for each variable:")
for column, count in na_counts.items():
    print(f"{column}: {count}")
