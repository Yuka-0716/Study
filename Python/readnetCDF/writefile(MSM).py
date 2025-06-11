#フォルダ内のMSMファイルをすべて読み込んで、任意の地点のデータを抽出し、出力ファイルに書き出す。修正版。
import netCDF4 as nc
import numpy as np
import os
from datetime import datetime, timedelta

# 入力フォルダと出力フォルダ
input_folder = "D:/Master/MSM(rawdata)/2024"
output_folder = "D:/Master/MSM(Himawari)/2024"

# 出力フォルダが存在しない場合は作成
os.makedirs(output_folder, exist_ok=True)

# ターゲット緯度・経度(ひまわり抽出点)
target_lat, target_lon = 32.75, 130.30

# NetCDFファイル一覧
nc_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".nc")])

# 各ファイル処理
for nc_file in nc_files:
    input_path = os.path.join(input_folder, nc_file)
    output_path = os.path.join(output_folder, f"{os.path.splitext(nc_file)[0]}data.txt")

    with nc.Dataset(input_path, 'r') as ds:
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        lat_idx = np.abs(lats - target_lat).argmin()
        lon_idx = np.abs(lons - target_lon).argmin()

        variables = [
            'psea', 'sp', 'u', 'v', 'temp', 'rh',
            'r1h', 'ncld_upper', 'ncld_mid', 'ncld_low', 'ncld', 'dswrf'
        ]

        time_var = ds.variables['time']
        times = time_var[:]
        time_units = time_var.units  # 例: "hours since 2022-01-01 00:00:00+00:00"
        time_str = time_units.split("since")[-1].strip().split("+")[0]
        base_time = datetime.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")

        # スケーリング関数（floatにキャスト）
        def apply_scale(var, val):
            scale = getattr(var, "scale_factor", 1.0)
            offset = getattr(var, "add_offset", 0.0)
            return float(val) * scale + offset

        # 欠損値チェック
        def is_missing(var, val):
            fill = getattr(var, "_FillValue", None)
            miss = getattr(var, "missing_value", None)
            if np.ma.is_masked(val) or val in [fill, miss] or np.isnan(val):
                return True
            return False

        # 出力ファイルにデータを書き込む
        with open(output_path, 'w') as f:
            # 実際の抽出座標を出力（確認用）
            actual_lat = lats[lat_idx]
            actual_lon = lons[lon_idx]
            f.write(f"# Extracted point: lat={actual_lat:.3f}, lon={actual_lon:.3f}\n")
            f.write("# Time psea sp u v temp rh r1h ncld_upper ncld_mid ncld_low ncld dswrf\n")

            for t_idx, time_val in enumerate(times):
                current_time = base_time + timedelta(hours=float(time_val))
                hhmm = current_time.strftime("%H%M")

                data_line = [hhmm]

                
                for var_name in variables:
                    var_data = ds.variables[var_name]
                    raw_value = var_data[t_idx, lat_idx, lon_idx]
                    
                    if np.ma.is_masked(raw_value):
                        data_line.append("N/A")
                    else:
                        scaled_value = float(raw_value)
                        if is_missing(var_data, scaled_value):
                            data_line.append("N/A")
                        else:
                            data_line.append(f"{scaled_value:.3f}")
                    
                f.write(" ".join(data_line) + "\n")

    print(f"Processed {nc_file} -> {output_path}")

print("All NetCDF files processed successfully.")
