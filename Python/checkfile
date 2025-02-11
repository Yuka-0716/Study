import netCDF4
import h5py

file_path = "E:\mesmodel_171205\mesmodel_171205\Z__C_RJTD_20171205000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin"

# NetCDFとして開けるか確認
try:
    with netCDF4.Dataset(file_path, 'r') as nc_data:
        print("ファイルはNetCDF形式です。".encode('utf-8').decode('utf-8'))
except OSError:
    print("NetCDF形式ではない可能性があります。".encode('utf-8').decode('utf-8'))

# HDF5として開けるか確認
try:
    with h5py.File(file_path, 'r') as hdf_data:
        print("ファイルはHDF5形式の可能性があります（NetCDF4形式の場合も含む）。".encode('utf-8').decode('utf-8'))
except OSError:
    print("ファイルはHDF5形式でもありません。".encode('utf-8').decode('utf-8'))
