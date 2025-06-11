#NetCDFファイルを読み込んで、各変数やファイルの詳細情報を取得

import netCDF4 as nec
import numpy as np
import matplotlib.pyplot as plt

# ファイルの移動後に新しいファイルパスに置き換え
loadfile = "E:/Master/MSM(rawdata)/2022/0101.nc"
HSDdata = nec.Dataset(loadfile, 'r')

# ファイルの基本情報を表示
print("netCDF データの情報:\n")
print(HSDdata)

# データセットの全変数を表示


# 各変数の情報を詳細表示
print("\n各変数の詳細情報:")
for var_name, var_data in HSDdata.variables.items():
    print(f"\n変数名: {var_name}")
    print(f"  次元: {var_data.dimensions}")
    print(f"  形状: {var_data.shape}")
    print(f"  データ型: {var_data.dtype}")
    if hasattr(var_data, 'long_name'):
        print(f"  説明: {var_data.long_name}")
    if hasattr(var_data, 'units'):
        print(f"  単位: {var_data.units}")
