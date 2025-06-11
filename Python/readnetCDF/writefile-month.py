#雲特性プロダクトから任意地点を含むグリッドのデータのみを抽出しテキストデータ化する。

import netCDF4 as nc
import numpy as np
import os

# 対象フォルダと出力ファイルのパス
input_folder = "D:/Master/JAXA/202403/"
output_file = "D:/Master/rawdata/202403_data.txt"

# 緯度・経度のターゲット値
target_lat, target_lon = 32.75, 130.30

# NetCDFファイルの名前から日時を取得する関数
def extract_date_and_time_from_filename(filepath):
    filename = os.path.basename(filepath)
    parts = filename.split('_')
    date_str = parts[2][:8]  # "20220326" の部分を取得
    time_str = parts[3][:4]  # "0000" の部分を取得
    return date_str, time_str

# フォルダ内のNetCDFファイルを再帰的に取得
file_list = []
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".nc"):
            file_list.append(os.path.join(root, file))

# ファイルを時系列順にソート
file_list.sort(key=lambda x: extract_date_and_time_from_filename(x)[0] + extract_date_and_time_from_filename(x)[1])

# データを出力ファイルに書き込む
with open(output_file, 'w') as f:
    for file_path in file_list:
        try:
            # NetCDFファイルを開く
            with nc.Dataset(file_path, 'r') as ds:
                # 緯度・経度を取得
                latitude = ds.variables['latitude'][:]
                longitude = ds.variables['longitude'][:]

                # 対応するインデックスを取得
                lat_index = np.abs(latitude - target_lat).argmin()
                lon_index = np.abs(longitude - target_lon).argmin()

                # 必要な変数
                variables_to_extract = ['Hour', 'CLOT', 'CLTT', 'CLTH', 'CLER_23', 'CLTYPE', 'QA']
                data_line = []

                # ファイル名から日付と時間を取得
                date_str, time_str = extract_date_and_time_from_filename(file_path)

                # 行の先頭に日付を追加
                data_line.append(date_str)

                for var_name in variables_to_extract:
                    var_data = ds.variables[var_name][:]

                    # 観測地点の値を取得
                    raw_value = var_data[lat_index, lon_index]

                    # 欠損値チェック
                    if np.ma.is_masked(raw_value) or raw_value == getattr(ds.variables[var_name], 'missing_value', None):
                        data_line.append("N/A")
                    else:
                        if var_name == "Hour":  # Hourにスケールファクターとオフセットを適用しHHMM形式に変換
                            scale_factor = getattr(ds.variables[var_name], 'scale_factor', 1.0)
                            add_offset = getattr(ds.variables[var_name], 'add_offset', 0.0)
                            adjusted_value = raw_value * scale_factor + add_offset
                            hours = int(adjusted_value)
                            minutes = round((adjusted_value - hours) * 60)
                            if minutes == 60:  # 繰り上げ処理
                                hours += 1
                                minutes = 0
                            formatted_value = f"{hours:02d}{minutes:02d}"
                            data_line.append(formatted_value)
                        else:  # 他の変数にはスケールファクターやオフセットを適用しない
                            data_line.append(str(raw_value))

                # ファイルごとのデータを出力ファイルに追記
                f.write(" ".join(data_line) + "\n")
        except OSError as e:
            print(f"Error processing file {file_path}: {e}")
        except KeyError as e:
            print(f"Missing variable in file {file_path}: {e}")

print(f"Data extracted and written to {output_file}")
