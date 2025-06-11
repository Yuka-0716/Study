#ひまわり標準データをまとめてNetCDF形式に変換

import subprocess
import glob

# 入力ファイルディレクトリと出力ディレクトリ
INPUT_DIR = "./himawari_files"
OUTPUT_DIR = "./netcdf_files"
CONVERTER_EXECUTABLE = "./convert_to_netcdf"  # Cプログラムの実行ファイルパス

def batch_convert_to_netcdf():
    """
    ひまわり標準データを一括でNetCDF形式に変換。
    """
    files = glob.glob(f"{INPUT_DIR}/*.dat")  # 標準データファイル拡張子に応じて調整
    for file in files:
        output_file = f"{OUTPUT_DIR}/{file.split('/')[-1].replace('.dat', '.nc')}"
        cmd = [CONVERTER_EXECUTABLE, file, output_file]
        subprocess.run(cmd, check=True)
        print(f"Converted: {file} -> {output_file}")

batch_convert_to_netcdf()
