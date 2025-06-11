#任意の複数地点を含む格子点の格子番号を表示

import netCDF4 as nc
import numpy as np

# NetCDFファイルのパス
file_path = "D:/Master/MSM(rawdata)/2022/0101.nc"

# NetCDFファイルを開く
ds = nc.Dataset(file_path)

# 緯度・経度の配列を取得
latitude = ds.variables['lat'][:]  # 1D配列または2D配列の可能性
longitude = ds.variables['lon'][:]

# 地点の辞書（緯度・経度）
points = {
    "地点1(ひまわりデータ抽出点)": (32.75, 130.30),
    "地点2(妙見岳駅)": (32.75625, 130.28568),
    "地点3(仁田峠駅)": (32.75088, 130.28554),
    "地点4(アメダス)": (32.442, 130.157), 
}

# 各地点のグリッドインデックスと対応する緯度経度を表示
grid_indices = {}
print("各地点のグリッドインデックスとその緯度・経度：")
for name, (lat, lon) in points.items():
    lat_index = np.abs(latitude - lat).argmin()
    lon_index = np.abs(longitude - lon).argmin()
    grid_indices[name] = (lat_index, lon_index)
    
    grid_lat = latitude[lat_index]
    grid_lon = longitude[lon_index]
    
    print(f"{name}: グリッドインデックス = ({lat_index}, {lon_index}), 緯度 = {grid_lat:.5f}, 経度 = {grid_lon:.5f}")

# すべて同じグリッドにあるか確認
unique_grids = set(grid_indices.values())
if len(unique_grids) == 1:
    print("\nすべての地点は同じグリッドに属しています。")
else:
    print("\nすべての地点は同じグリッドに属していません。")

# NetCDFファイルを閉じる
ds.close()
