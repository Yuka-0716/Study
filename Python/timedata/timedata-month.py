import matplotlib.pyplot as plt
from datetime import datetime

# データファイルのパス
input_file = "D:/Master/202203/202203_data.txt"

# データの読み込み
data = []
with open(input_file, 'r') as f:
    for line in f:
        # 各行を分割し、データを格納
        parts = line.strip().split()
        if "N/A" in parts:  # 欠損値が含まれる場合はスキップ
            continue
        try:
            # 日付と時間が正しい形式であるかを確認
            date = parts[0]
            time = parts[1].zfill(4)  # 時間をゼロ埋め
            datetime.strptime(f"{date} {time}", "%Y%m%d %H%M")  # フォーマット確認
            data.append([float(p) if i > 1 else p for i, p in enumerate(parts)])  # 日付と時間はそのまま保持
        except ValueError:
            # 日付や時間が不正な場合はスキップ
            print(f"Skipping invalid row: {line.strip()}")
            continue

# 列ごとにデータを分割
columns = list(zip(*data))

# 1列目と2列目を結合して時系列データを作成（横軸）
datetime_series = [
    datetime.strptime(f"{date} {time.zfill(4)}", "%Y%m%d %H%M") for date, time in zip(columns[0], columns[1])
]

# 縦軸（3列目から8列目）
variables = {
    "Optical Thickness (CLOT)": columns[2],
    "Cloud Top Temperature (CLTT)": columns[3],
    "Cloud Top Height (CLTH)": columns[4],
    "Effective Radius (CLER_23)": columns[5],
    "Cloud Type (CLTYPE)": columns[6],
    "Quality Assurance (QA)": columns[7]
}

# 各変数ごとにグラフを作成
for var_name, y in variables.items():
    plt.figure(figsize=(10, 6))
    plt.plot(datetime_series, y, marker='o', label=var_name)
    plt.title(f"Time Series of {var_name}", fontsize=14)
    plt.xlabel("Datetime", fontsize=12)
    plt.ylabel(var_name, fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)  # 日時を見やすく回転
    plt.show()

print("Done.")
