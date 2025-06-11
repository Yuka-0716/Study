import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# ファイルパス
amedas_path = r"D:/Master/tempdata/202203-202404.temp.txt"
msm_folder = r"D:/Master/MSM/2024"

# AMeDASデータ読み込み
amedas_df = pd.read_csv(amedas_path, delim_whitespace=True, names=["day", "hour", "temp"])
amedas_df["day_suffix"] = amedas_df["day"].astype(str).str[-4:]

# MSMフォルダ内のファイル一覧を取得（昇順）
msm_files = sorted(glob.glob(os.path.join(msm_folder, "????data.txt")))

# MSMのカラム名
msm_columns = [
    "hour", "psea", "sp", "u", "v", "temp", "rh",
    "r1h", "ncld_upper", "ncld_mid", "ncld_low", "ncld", "dswrf"
]

# 結合用リストを初期化
merged_list = []
total_plot_count = 0  # 合計プロット数

# 各 MSM ファイルを順に処理
for msm_path in msm_files:
    msm_filename = os.path.basename(msm_path)
    msm_day_suffix = msm_filename[:4]  # 例: "0401"

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
        skiprows=2  # ヘッダー行2行をスキップ
    )

    # MSM 側の温度列を明示的に変更
    msm_df = msm_df.rename(columns={"temp": "temp_msm"})

    # hourで結合（suffix指定は不要になる）
    merged_df = pd.merge(amedas_filtered, msm_df, on="hour")


    # データを追加して、情報を表示
    merged_list.append(merged_df[["temp_amedas", "temp_msm"]])
    plot_count = len(merged_df)
    total_plot_count += plot_count
    print(f"[読み込み] {msm_path}：{plot_count} 件のプロットを追加")

# すべてまとめて結合
if not merged_list:
    print("一致するデータがありませんでした。")
else:
    total_df = pd.concat(merged_list, ignore_index=True)

    print(f"\n✅ 全ファイルの合計プロット数：{total_plot_count} 件")

    # ▶ 平均誤差（Mean Error）の計算
    error = total_df["temp_msm"] - total_df["temp_amedas"]
    mean_error = error.mean()
    print(f"📏 平均誤差（Mean Error）：{mean_error:.3f} (°C)")

    # 散布図を1枚で描画
    plt.figure(figsize=(6, 6))
    plt.scatter(
        total_df["temp_amedas"],
        total_df["temp_msm"],
        color='black',
        s=0.1
    )

    # y = x の赤線
    min_temp = min(total_df["temp_amedas"].min(), total_df["temp_msm"].min())
    max_temp = max(total_df["temp_amedas"].max(), total_df["temp_msm"].max())
    plt.plot([min_temp, max_temp], [min_temp, max_temp], color='red')

    # ラベルなど
    plt.xlabel("AMeDAS Temperature (°C)")
    plt.ylabel("MSM Temperature (°C)")
    plt.title("AMeDAS vs MSM Temperature (All Days Combined)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
