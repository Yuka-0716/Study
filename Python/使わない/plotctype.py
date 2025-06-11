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
CLTYPE = ds.variables['CLTYPE'][:]

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
CLTYPE_subset = CLTYPE[lat_indices.min():lat_indices.max() + 1,
                       lon_indices.min():lon_indices.max() + 1]

# 雲相判定
cloud_phase = np.full(CLOT_subset.shape, -1)  # 初期化 (-1: 未分類)
cloud_phase[CLOT_subset > 7000] = 2  # 厚い雲（CLOTが7000以上）
cloud_phase[(CLOT_subset >= 3000) & (CLOT_subset <= 7000)] = 1  # 薄い雲
cloud_phase[CLOT_subset < 3000] = 0  # 雲なし

# プロット - 雲相
plt.figure(figsize=(12, 6))

# サブプロット 1: 雲相
plt.subplot(1, 2, 1)
plt.imshow(cloud_phase, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='viridis')
plt.colorbar(label='Cloud Phase')
plt.title('Cloud Phase over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# 雲タイプのラベル
cloud_types = {
    0: 'Clear',
    1: 'Ci (Cirrus)',
    2: 'Cs (Stratus)',
    3: 'Deep convection',
    4: 'Ac (Altostratus)',
    5: 'As (Asperitas)',
    6: 'Ns (Nimbostratus)',
    7: 'Cu (Cumulus)',
    8: 'Sc (Stratocumulus)',
    9: 'St (Stratus)',
    10: 'Unknown'
}

# プロット - 雲タイプ
plt.subplot(1, 2, 2)
plt.imshow(CLTYPE_subset, extent=[lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
           origin='lower', cmap='tab20b')
plt.colorbar(label='Cloud Type')
plt.title('Cloud Type over Mt. Myoken')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.tight_layout()
plt.show()
