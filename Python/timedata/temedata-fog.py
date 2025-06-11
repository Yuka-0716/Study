import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス
input_file = "C:/Users/bb40120052/Desktop/Python/.vscode/202203-fog.txt"

# データの読み込み
data = pd.read_csv(input_file, sep="\t", header=None, 
                   names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"], na_values="N/A")

# 時間の統合
data["Timestamp"] = pd.to_datetime(data["days"].astype(str) + data["Hour"].astype(str).str.zfill(4), format="%Y%m%d%H%M")

# 描画する列
target_columns = ["CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE"]

# 時系列プロット
plt.figure(figsize=(12, 8))
for column in target_columns:
    plt.plot(data["Timestamp"], data[column], label=column, marker='o')

# グラフの設定
plt.title("Time Series of Selected Columns")
plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.legend()
plt.grid(True)
plt.tight_layout()

# プロットの表示
plt.show()
