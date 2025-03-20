#Webページのすべてのファイルを、任意のパスにダウンロード

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 設定
base_url = "https://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/netcdf/MSM-S/2024/"
save_dir = r"E:/Master/MSM(rawdata)/2024"

# 保存フォルダが存在しない場合は作成
os.makedirs(save_dir, exist_ok=True)

# HTMLを取得して解析
response = requests.get(base_url)
if response.status_code != 200:
    print(f"Failed to access {base_url}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# ファイルリンクを取得
file_links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".nc"):  # NetCDFファイルのみ対象
        file_links.append(urljoin(base_url, href))

# ダウンロード処理
for file_url in file_links:
    file_name = os.path.basename(file_url)
    save_path = os.path.join(save_dir, file_name)

    if os.path.exists(save_path):
        print(f"Already exists: {file_name}, skipping...")
        continue

    print(f"Downloading {file_name}...")
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Saved: {save_path}")

print("Download completed.")
