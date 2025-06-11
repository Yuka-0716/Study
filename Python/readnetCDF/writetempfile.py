import csv
from datetime import datetime

# 入力ファイルパスと出力ファイルパス
input_file = r"D:/Master/202303雲仙岳気温.csv"
output_file = "D:/Master/2023temp.txt"

try:
    # CSVファイルを読み込み
    with open(input_file, mode='r', encoding='shift_jis') as csvfile:
        reader = csv.reader(csvfile)

        # 出力ファイルに書き込み
        with open(output_file, mode='w', encoding='utf-8') as outfile:
            for row in reader:
                if len(row) < 2:
                    continue  # データが2列未満の場合はスキップ

                datetime_original = row[0]
                temperature = row[1]

                try:
                    # 日時をdatetimeでパースし、フォーマットを統一
                    dt = datetime.strptime(datetime_original, "%Y/%m/%d %H:%M")
                    combined_date = dt.strftime("%Y%m%d")
                    time_part = dt.strftime("%H%M")  # ← ここが4桁保証

                    temperature_kelvin = float(temperature) + 273.15

                    # 出力フォーマット：年月日 時刻 気温(K)
                    formatted_line = f"{combined_date} {time_part} {temperature_kelvin:.2f}\n"
                    outfile.write(formatted_line)
                except Exception:
                    print(f"日時データの変換に失敗しました: {datetime_original}")
except FileNotFoundError:
    print(f"入力ファイルが見つかりません: {input_file}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
