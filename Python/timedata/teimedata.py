import matplotlib.pyplot as plt

# データファイルのパス
input_file = "C:/Users/bb40120052/Desktop/Python/.vscode/Master/20220301_data.txt"

# データの読み込み
data = []
with open(input_file, 'r') as f:
    for line in f:
        # 各行を分割し、データを格納
        parts = line.strip().split()
        if "N/A" in parts:  # 欠損値が含まれる場合はスキップ
            continue
        data.append([float(p) if i > 0 else p for i, p in enumerate(parts)])  # 1列目はそのまま文字列で保持

# 列ごとにデータを分割
columns = list(zip(*data))

# 横軸（1列目：時間）
x = columns[0]

# 縦軸（2列目以降）
variables = {
    "CLOT": columns[1],
    "CLTT": columns[2],
    "CLTH": columns[3],
    "CLER_23": columns[4],
    "CLTYPE": columns[5],
    "QA": columns[6]
}

# 各変数ごとにグラフを作成
for var_name, y in variables.items():
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', label=var_name)
    plt.title(f"Time Series of {var_name}", fontsize=14)
    plt.xlabel("Time (HHMM)", fontsize=12)
    plt.ylabel(var_name, fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

print("Done.")
