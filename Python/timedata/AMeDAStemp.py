#アメダスの気温について時系列の図を描くimport pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

# アメダス気温データのファイルパス
amedas_path = r"D:/Master/tempdata/202203-202404.temp.txt"

# データ読み込み（区切りはスペースやタブを想定）
amedas_df = pd.read_csv(amedas_path, delim_whitespace=True, names=["day", "hour", "temp"])

# hour を4桁に（例：900 → "0900"）
amedas_df["hour"] = amedas_df["hour"].astype(str).str.zfill(4)

# Timestamp（日時）を作成
amedas_df["Timestamp"] = pd.to_datetime(amedas_df["day"].astype(str) + amedas_df["hour"], format="%Y%m%d%H%M")

# 時系列で並び替え（念のため）
amedas_df = amedas_df.sort_values("Timestamp").reset_index(drop=True)

# 時系列プロット
plt.figure(figsize=(12, 6))
plt.plot(amedas_df["Timestamp"], amedas_df["temp"], color='orange', linewidth=1)

# ラベル設定
plt.title("Time Series of AMeDAS Temperature")
plt.xlabel("Timestamp")
plt.ylabel("Temperature (K)")  # 摂氏
plt.grid(True)
plt.tight_layout()
plt.show()
