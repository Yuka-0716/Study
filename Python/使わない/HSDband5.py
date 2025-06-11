import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

# NetCDFファイルの読み込み
file_path = 'C:/Users/bb40120052/Desktop/Python/.vscode/Master/output.nc'
ds = nc.Dataset(file_path)

# 変数の読み込み
latitude = ds.variables['latitude'][:]
longitude = ds.variables['longitude'][:]
albedo = ds.variables['albedo'][:]

# 妙見岳の周辺座標を選択
center_lat, center_lon = 32.75, 130.30
lat_range = (center_lat - 0.1, center_lat + 0.1)
lon_range = (center_lon - 0.1, center_lon + 0.1)

# 対象範囲のインデックスを取得
lat_indices = np.where((latitude >= lat_range[0]) & (latitude <= lat_range[1]))[0]
lon_indices = np.where((longitude >= lon_range[0]) & (longitude <= lon_range[1]))[0]

# 対象範囲のデータを切り出し
albedo_subset = albedo[lat_indices.min():lat_indices.max() + 1,
                       lon_indices.min():lon_indices.max() + 1]

# 雲相判定
cloud_phase = np.full(albedo_subset.shape, -1)  # 初期化 (-1: 未分類)
cloud_phase[albedo_subset > 0.7] = 2  # 厚い雲
cloud_phase[(albedo_subset >= 0.4) & (albedo_subset <= 0.7)] = 1  # 薄い雲
cloud_phase[albedo_subset < 0.4] = 0  # 雲なし

# プロット
plt.figure(figsize=(8, 6))
plt.imshow(cloud_phase, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='viridis')
plt.colorbar(label='Cloud Phase')
plt.title('Cloud Phase over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# 観測時刻の取得
#import datetime

#start_time = ds.variables['start_time'][:]
#start_time_units = ds.variables['start_time'].units
#start_datetime = nc.num2date(start_time, units=start_time_units)

#print("Observation start time:", start_datetime)
