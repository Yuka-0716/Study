import os
import pandas as pd

def process_fog_data(cloud_dir, temp_dir, output_file):
    # ファイルパスの確認
    cloud_files = [cloud_dir] if os.path.isfile(cloud_dir) else [os.path.join(cloud_dir, f) for f in os.listdir(cloud_dir) if f.endswith('.txt')]
    temp_files = [temp_dir] if os.path.isfile(temp_dir) else [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.txt')]

    print(f"Cloud files: {cloud_files}")
    print(f"Temp files: {temp_files}")

    # 符合するデータの格納
    matched_data = []

    # ファイルを読み込む
    for cloud_file in cloud_files:
        for temp_file in temp_files:
            # ファイルの存在確認
            if not (os.path.isfile(cloud_file) and os.path.isfile(temp_file)):
                print(f"Error: File not found - {cloud_file} or {temp_file}")
                continue

            print(f"Processing Cloud File: {cloud_file}, Temp File: {temp_file}")

            # ファイルの読み込み
            try:
                cloud_data = pd.read_csv(cloud_file, delim_whitespace=True, header=None, 
                                         names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"], usecols=[0, 1, 2, 3, 4, 5, 6, 7])
                temp_data = pd.read_csv(temp_file, delim_whitespace=True, header=None, 
                                        names=["days", "Hour", "CLTT"], usecols=[0, 1, 2])
            except Exception as e:
                print(f"Error reading files: {e}")
                continue

            print(f"Cloud Data: {len(cloud_data)} rows, Temp Data: {len(temp_data)} rows")

            # 条件を適用したデータの格納
            for _, cloud_row in cloud_data.iterrows():
                for _, temp_row in temp_data.iterrows():
                    if (int(cloud_row["days"]) == int(temp_row["days"])) and (cloud_row["Hour"] == temp_row["Hour"]):
                        try:
                            if float(temp_row["CLTT"]) - float(cloud_row["CLTT"]) <= 12:
                                matched_data.append([
                                    int(cloud_row["days"]),
                                    str(int(float(cloud_row["Hour"]))).zfill(4),
                                    cloud_row["CLOT"] if pd.notna(cloud_row["CLOT"]) else "N/A",
                                    cloud_row["CLTT"] if pd.notna(cloud_row["CLTT"]) else "N/A",
                                    cloud_row["CLTH"] if pd.notna(cloud_row["CLTH"]) else "N/A",
                                    cloud_row["CLER_23"] if pd.notna(cloud_row["CLER_23"]) else "N/A",
                                    cloud_row["CTYPE"] if pd.notna(cloud_row["CTYPE"]) else "N/A",
                                    cloud_row["QA"] if pd.notna(cloud_row["QA"]) else "N/A"
                                ])
                        except (ValueError, TypeError):
                            print(f"Error processing row: {cloud_row}")
                            continue

    # ファイルに書き込み
    if matched_data:
        matched_df = pd.DataFrame(matched_data, columns=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"])
        matched_df.to_csv(output_file, sep="\t", index=False, header=False, float_format='%.6g')
        print(f"Matching data has been written to {output_file}")
    else:
        print("No matching data found.")

# 最初の処理
process_fog_data(
    cloud_dir="D:/Master/rawdata/202203_data.txt",
    temp_dir="D:/Master/tempdata/202203-202404.temp.txt",
    output_file="D:/Master/FogData/FogData(12)/202203-fog.txt"
)

# 次のセットの処理
process_fog_data(
    cloud_dir="D:/Master/rawdata/202204_data.txt",
    temp_dir="D:/Master/tempdata/202203-202404.temp.txt",
    output_file="D:/Master/FogData/FogData(12)/202204-fog.txt"
)

process_fog_data(
    cloud_dir="D:/Master/rawdata/202205_data.txt",
    temp_dir="D:/Master/tempdata/202203-202404.temp.txt",
    output_file="D:/Master/FogData/FogData(12)/202205-fog.txt"
)

process_fog_data(
    cloud_dir="D:/Master/rawdata/202206_data.txt",
    temp_dir="D:/Master/tempdata/202203-202404.temp.txt",
    output_file="D:/Master/FogData/FogData(12)/202206-fog.txt"
)
