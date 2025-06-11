import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# ファイルパス
cloud_dir = "E:/Master/rawdata/202204_data.txt"
temp_dir = "C:/Users/bb40120052/Desktop/Python/.vscode/2022.temp.txt"

# 両方のファイルを確認
cloud_files = [cloud_dir] if os.path.isfile(cloud_dir) else [os.path.join(cloud_dir, f) for f in os.listdir(cloud_dir) if f.endswith('.txt')]
temp_files = [temp_dir] if os.path.isfile(temp_dir) else [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.txt')]

# 符合するデータの結果を格納
matched_rows = []

# ファイルを読み込む
for cloud_file in cloud_files:
    for temp_file in temp_files:
        # ファイルの読み込み
        cloud_data = pd.read_csv(cloud_file, delim_whitespace=True, header=None, 
                                 names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"], usecols=[0, 1, 2, 3, 4, 5, 6, 7])
        temp_data = pd.read_csv(temp_file, delim_whitespace=True, header=None, 
                                names=["days", "Hour", "CLTT"], usecols=[0, 1, 2])

        # 特殊条件に適用するための関数
        def check_hour_match(cloud_hour, temp_hour, cloud_day, temp_day):
            try:
                # cloud_hourとtemp_hourの整数化と上2桁抽出
                cloud_hour_prefix = int(str(int(float(cloud_hour)))[:2])
                temp_hour_prefix = int(str(int(float(temp_hour)))[:2])
            except (ValueError, TypeError):
                return False

            # 普通の条件: temp_dir Hourの上2桁 - 1 == cloud_dir Hourの上2桁
            if temp_hour_prefix != 0:
                return temp_hour_prefix - 1 == cloud_hour_prefix
            else:
                # 特殊条件: temp_dir Hourの上2桁 == 00の場合
                return (cloud_hour_prefix == 23) and (cloud_day == temp_day - 1)

        # 特殊条件を適用したデータの符合
        for _, cloud_row in cloud_data.iterrows():
            for _, temp_row in temp_data.iterrows():
                if check_hour_match(cloud_row["Hour"], temp_row["Hour"], cloud_row["days"], temp_row["days"]):
                    try:
                        if abs(float(cloud_row["CLTT"]) - float(temp_row["CLTT"])) <= 3:
                            matched_rows.append([
                                int(cloud_row["days"]), int(float(cloud_row["Hour"])), cloud_row["CLOT"],
                                cloud_row["CLTT"], cloud_row["CLTH"], cloud_row["CLER_23"]
                            ])
                    except (ValueError, TypeError):
                        continue

# グラフ用のデータの変換
if matched_rows:
    matched_df = pd.DataFrame(matched_rows, columns=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23"])
    matched_df["Datetime"] = matched_df.apply(lambda row: datetime.strptime(f"{int(row['days'])} {str(int(row['Hour'])).zfill(4)}", "%Y%m%d %H%M"), axis=1)
    matched_df.sort_values(by="Datetime", inplace=True)

    # 時系列データのプロット
    plt.figure(figsize=(10, 6))
    plt.plot(matched_df["Datetime"], matched_df["CLOT"], label="CLOT (Optical Thickness)")
    plt.plot(matched_df["Datetime"], matched_df["CLTT"], label="CLTT (Cloud Top Temperature)")
    plt.plot(matched_df["Datetime"], matched_df["CLTH"], label="CLTH (Cloud Top Height)")
    plt.plot(matched_df["Datetime"], matched_df["CLER_23"], label="CLER_23 (Effective Radius)")

    plt.title("Time Series of Cloud Properties")
    plt.xlabel("Datetime")
    plt.ylabel("Values")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No matching data found.")

# 結果の表示
print(f"Number of matching datasets: {len(matched_rows)}")
