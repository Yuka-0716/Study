#ひまわり雲特性プロダクトの一時間分のデータセットを読み込み、任意地点のデータをまとめてテキストファイル化

import netCDF4 as nc
import numpy as np
import os

# 対象フォルダと出力ファイルのパス
input_folder = "D:/Master/202203/01/00/"
output_file = "output_data.txt"

# 緯度・経度のターゲット値
target_lat, target_lon = 32.75, 130.30

# NetCDFファイルの名前から日時を取得する関数
def extract_datetime_from_filename(filename):
    parts = filename.split('_')
    datetime_str = parts[1] + "_" + parts[2][:4]  # "20220303_1850" の部分を取得
    return datetime_str

# フォルダ内のNetCDFファイルを取得し、時系列順に並び替える
file_list = [f for f in os.listdir(input_folder) if f.endswith(".nc")]
file_list.sort(key=extract_datetime_from_filename)  # 時系列順にソート

# データを出力ファイルに書き込む
with open(output_file, 'w') as f:
    for file_name in file_list:
        file_path = os.path.join(input_folder, file_name)
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

print(f"Data extracted and written to {output_file}")
