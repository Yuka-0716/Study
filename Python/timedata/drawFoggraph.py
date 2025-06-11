#ひまわり雲特性プロダクトから任意地点のみ抽出したテキストファイルの各変数について時系列変化の図を描く
import pandas as pd
import matplotlib.pyplot as plt

# ファイルパス
input_file = "D:/Master/FogData/FogData(12)/202203-fog.txt"

# データの読み込み
data = pd.read_csv(input_file, sep="\t", header=None, 
                   names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"], na_values="N/A")

# 時間の統合
data["Timestamp"] = pd.to_datetime(data["days"].astype(str) + data["Hour"].astype(str).str.zfill(4), format="%Y%m%d%H%M")

# 描画する列
target_columns = ["CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE"]

# 各変数ごとに時系列プロット
for column in target_columns:
    plt.figure(figsize=(10, 6))
    plt.plot(data["Timestamp"], data[column], label=column, marker='o')
    
    # グラフの設定
    plt.title(f"Time Series of {column}")
    plt.xlabel("Timestamp")
    plt.ylabel(column)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # プロットの表示
    plt.show()
