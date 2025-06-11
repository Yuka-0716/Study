import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# ファイルパス
amedas_path = r"D:/Master/tempdata/202203-202404.temp.txt"
msm_folder = r"D:/Master/MSM/2022"

# AMeDASデータ読み込み
amedas_df = pd.read_csv(amedas_path, delim_whitespace=True, names=["day", "hour", "temp"])
amedas_df["day_suffix"] = amedas_df["day"].astype(str).str[-4:]
amedas_df["month"] = amedas_df["day"].astype(str).str[:6]  # e.g. 202404

# MSMフォルダ内のファイル一覧を取得（昇順）
msm_files = sorted(glob.glob(os.path.join(msm_folder, "????data.txt")))

# MSMのカラム名
msm_columns = [
    "hour", "psea", "sp", "u", "v", "temp", "rh",
    "r1h", "ncld_upper", "ncld_mid", "ncld_low", "ncld", "dswrf"
]

# 月ごとの結合結果を保存する辞書
monthly_data = {}

# 各 MSM ファイルを順に処理
for msm_path in msm_files:
    msm_filename = os.path.basename(msm_path)
    msm_day_suffix = msm_filename[:4]  # 例: "0401"
    msm_day_full = f"2024{msm_day_suffix}"  # 例: "20240401"
    msm_month = msm_day_full[:6]  # e.g. "202404"

    # AMeDASから対象日付のデータを抽出
    amedas_filtered = amedas_df[amedas_df["day_suffix"] == msm_day_suffix]
    if amedas_filtered.empty:
        print(f"[スキップ] {msm_filename}：AMeDASに対応データなし")
        continue

    # 同じhourが複数ある場合は平均を取る
    amedas_filtered = (
        amedas_filtered.groupby("hour", as_index=False)["temp"]
        .mean()
        .rename(columns={"temp": "temp_amedas"})
    )

    # MSMファイル読み込み
    msm_df = pd.read_csv(
        msm_path,
        delim_whitespace=True,
        names=msm_columns,
        comment='#',
        skiprows=2
    )
    msm_df = msm_df.rename(columns={"temp": "temp_msm"})

    # hourで結合
    merged_df = pd.merge(amedas_filtered, msm_df, on="hour")
    if merged_df.empty:
        print(f"[スキップ] {msm_filename}：hour一致データなし")
        continue

    # 月ごとのリストに追加
    if msm_month not in monthly_data:
        monthly_data[msm_month] = []
    monthly_data[msm_month].append(merged_df[["temp_amedas", "temp_msm"]])

    print(f"[読み込み] {msm_path}：{len(merged_df)} 件のプロットを追加")

# 月別に処理
for month, dfs in monthly_data.items():
    monthly_df = pd.concat(dfs, ignore_index=True)
    total_points = len(monthly_df)

    error = monthly_df["temp_msm"] - monthly_df["temp_amedas"]
    mean_error = error.mean()

    print(f"\n📅 月：{month} | 件数：{total_points} | 平均誤差：{mean_error:.3f} °C")

    # 散布図を描画
    plt.figure(figsize=(6, 6))
    plt.scatter(
        monthly_df["temp_amedas"],
        monthly_df["temp_msm"],
        color='black',
        s=0.1
    )

    # y = x の赤線
    min_temp = min(monthly_df["temp_amedas"].min(), monthly_df["temp_msm"].min())
    max_temp = max(monthly_df["temp_amedas"].max(), monthly_df["temp_msm"].max())
    plt.plot([min_temp, max_temp], [min_temp, max_temp], color='red')

    plt.xlabel("AMeDAS Temperature (°C)")
    plt.ylabel("MSM Temperature (°C)")
    plt.title(f"AMeDAS vs MSM Temperature - {month}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
