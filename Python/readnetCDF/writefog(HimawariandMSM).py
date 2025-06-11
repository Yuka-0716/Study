#ひまわり雲特性プロダクトのCTTとMSM気温の差が12度以内かつひまわり雲特性プロダクトのCLTHが2km以下のデータを霧として出力

import os
import pandas as pd

def process_fog_data(cloud_file, temp_dir, output_file):
    if not os.path.isfile(cloud_file):
        print(f"Cloud file not found: {cloud_file}")
        return

    # cloudファイル読み込み
    cloud_df = pd.read_csv(
        cloud_file,
        sep=r'\s+',
        header=None,
        names=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"],
        dtype=str  # すべて文字列として読み込む
    )
    print(f"Loaded {len(cloud_df)} cloud records")

    # tempファイル一覧
    temp_files = sorted([
        os.path.join(temp_dir, f)
        for f in os.listdir(temp_dir)
        if f.lower().endswith("data.txt") and len(f) >= 8
    ])

    matched_data = []

    # ログカウンタ
    skipped_cloud_rows = 0
    skipped_temp_rows = 0
    total_cloud_rows = 0
    total_temp_rows = 0

    for temp_file in temp_files:
        mmdd = os.path.basename(temp_file)[:4]
        matching_cloud = cloud_df[cloud_df["days"].str[4:] == mmdd]

        if matching_cloud.empty:
            continue

        try:
            temp_df = pd.read_csv(
                temp_file,
                sep=r'\s+',
                header=None,
                names=[
                    "hour", "psea", "sp", "u", "v", "temp", "rh",
                    "r1h", "ncld_upper", "ncld_mid", "ncld_low", "ncld", "dswrf", "extra"
                ],
                engine='python'
            )
        except Exception as e:
            print(f"Error reading {temp_file}: {e}")
            continue

        for _, cloud_row in matching_cloud.iterrows():
            total_cloud_rows += 1
            try:
                cltt = float(cloud_row["CLTT"])
                clth = float(cloud_row["CLTH"])

                if pd.isna(cltt) or pd.isna(clth) or clth > 2:
                    skipped_cloud_rows += 1
                    continue

                cloud_hour_prefix = str(int(float(cloud_row["Hour"]))).zfill(4)[:2]
                temp_matches = temp_df[temp_df["hour"].astype(str).str.zfill(4).str[:2] == cloud_hour_prefix]

                matched = False
                for _, temp_row in temp_matches.iterrows():
                    total_temp_rows += 1
                    try:
                        temp_val_raw = temp_row["temp"]
                        if pd.isna(temp_val_raw) or temp_val_raw is None:
                            skipped_temp_rows += 1
                            continue
                        temp_val = float(temp_val_raw)
                        if abs(temp_val - cltt) <= 12:
                            matched_data.append([
                                cloud_row["days"].zfill(8),
                                str(int(float(cloud_row["Hour"]))).zfill(4),
                                cloud_row["CLOT"],
                                cltt,
                                clth,
                                cloud_row["CLER_23"],
                                cloud_row["CTYPE"],
                                cloud_row["QA"]
                            ])
                            matched = True
                            break
                        else:
                            skipped_temp_rows += 1
                    except Exception:
                        skipped_temp_rows += 1
                        continue
                if not matched:
                    skipped_cloud_rows += 1
            except Exception:
                skipped_cloud_rows += 1
                continue

    # 出力
    if matched_data:
        df = pd.DataFrame(
            matched_data,
            columns=["days", "Hour", "CLOT", "CLTT", "CLTH", "CLER_23", "CTYPE", "QA"]
        )
        df.to_csv(output_file, sep="\t", index=False, header=False, float_format='%.6g')
        print(f"{len(df)} records written to {output_file}")
    else:
        print("No matching data found.")

    # ログ出力
    print("\n--- Summary Report ---")
    print(f"Total cloud rows processed: {total_cloud_rows}")
    print(f"  → Skipped cloud rows (missing/CLTH>2/invalid): {skipped_cloud_rows}")
    print(f"Total temp rows attempted: {total_temp_rows}")
    print(f"  → Skipped temp rows (invalid/mismatch): {skipped_temp_rows}")

# 使用例（2022年3月）
process_fog_data(
    cloud_file="D:/Master/rawdata/202403_data.txt",
    temp_dir="D:/Master/MSM(Himawari)/2024",
    output_file="D:/Master/FogData/FogData(12)/202403-fog.txt"
)
