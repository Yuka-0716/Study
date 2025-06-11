#NetCDF形式のひまわり標準データを読み込み、任意の地点の放射輝度をプロット

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
nc_files = 'C:/Users/bb40120052/Desktop/Python/.vscode/Master/NC_H08_20220301_0000_L2CLP010_FLDK.02401_02401.nc'
# 指定地点（雲仙妙見岳）の緯度・経度
TARGET_LAT = 32.8439
TARGET_LON = 130.3736

def plot_time_series(nc_files):
    """
    NetCDFファイル群から指定地点の時系列データをプロット。
    Args:
        nc_files (list): NetCDFファイルのパスリスト
    """
    times = []
    values = []

    for file in nc_files:
        with nc.Dataset(file) as ds:
            # 緯度・経度に最も近いインデックスを取得
            lats = ds.variables['latitude'][:]
            lons = ds.variables['longitude'][:]
            time = ds.variables['time'][:]
            data = ds.variables['data_variable'][:]  # データ変数を適宜変更

            lat_idx = np.abs(lats - TARGET_LAT).argmin()
            lon_idx = np.abs(lons - TARGET_LON).argmin()

            times.extend(time)
            values.extend(data[:, lat_idx, lon_idx])

    # 時系列プロット
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o')
    plt.title("Time Series at Unzen Myoken Peak")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid()
    plt.show()

# 例: NetCDFファイルリスト
nc_files = ["file1.nc", "file2.nc", "file3.nc"]  # 適切に変更
plot_time_series(nc_files)
