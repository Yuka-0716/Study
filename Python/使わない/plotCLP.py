import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

# NetCDFファイルの読み込み
file_path = 'C:/Users/bb40120052/Desktop/Python/.vscode/Master/NC_H08_20220301_0000_L2CLP010_FLDK.02401_02401.nc'
ds = nc.Dataset(file_path)

# 変数の読み込み
latitude = ds.variables['latitude'][:]
longitude = ds.variables['longitude'][:]
CLOT = ds.variables['CLOT'][:]
CLTT = ds.variables['CLTT'][:]
CLTH = ds.variables['CLTH'][:]
CLER_23 = ds.variables['CLER_23'][:]

# 妙見岳の周辺座標を選択
center_lat, center_lon = 32.75, 130.30
lat_range = (center_lat - 0.1, center_lat + 0.1)
lon_range = (center_lon - 0.1, center_lon + 0.1)

# 対象範囲のインデックスを取得
lat_indices = np.where((latitude >= lat_range[0]) & (latitude <= lat_range[1]))[0]
lon_indices = np.where((longitude >= lon_range[0]) & (longitude <= lon_range[1]))[0]

# 対象範囲のデータを切り出し
CLOT_subset = CLOT[lat_indices.min():lat_indices.max() + 1,
                   lon_indices.min():lon_indices.max() + 1]
CLTT_subset = CLTT[lat_indices.min():lat_indices.max() + 1,
                   lon_indices.min():lon_indices.max() + 1]
CLTH_subset = CLTH[lat_indices.min():lat_indices.max() + 1,
                   lon_indices.min():lon_indices.max() + 1]
CLER_23_subset = CLER_23[lat_indices.min():lat_indices.max() + 1,
                         lon_indices.min():lon_indices.max() + 1]

# プロット - CLOT（雲光学的厚さ）
plt.figure(figsize=(8, 6))
plt.imshow(CLOT_subset, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='viridis')
plt.colorbar(label='Cloud Optical Thickness')
plt.title('Cloud Optical Thickness over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# プロット - CLTT（雲頂温度）
plt.figure(figsize=(8, 6))
plt.imshow(CLTT_subset, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='coolwarm')
plt.colorbar(label='Cloud Top Temperature (K)')
plt.title('Cloud Top Temperature over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# プロット - CLTH（雲頂高さ）
plt.figure(figsize=(8, 6))
plt.imshow(CLTH_subset, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='YlGnBu')
plt.colorbar(label='Cloud Top Height (km)')
plt.title('Cloud Top Height over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# プロット - CLER_23（雲効果半径）
plt.figure(figsize=(8, 6))
plt.imshow(CLER_23_subset, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='Blues')
plt.colorbar(label='Cloud Effective Radius (μm)')
plt.title('Cloud Effective Radius using Band 6 over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
