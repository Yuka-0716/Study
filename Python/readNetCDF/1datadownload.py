from ftplib import FTP
import os

# FTP接続情報
FTP_SERVER = "example.ftp.server"
FTP_USER = "your_username"
FTP_PASS = "your_password"
REMOTE_DIR = "/path/to/data"  # サーバ上のデータディレクトリ
LOCAL_DIR = "./downloaded_files"  # ローカル保存先

def download_files(date_list, band_list):
    """
    指定された日時範囲とバンドのデータを一括ダウンロード。
    Args:
        date_list (list): 日時のリスト（例: ['20241115', '20241116']）
        band_list (list): バンド番号のリスト（例: ['B03', 'B08']）
    """
    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)
    
    with FTP(FTP_SERVER) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_DIR)
        files = ftp.nlst()  # ディレクトリ内のファイル一覧取得
        
        for date in date_list:
            for band in band_list:
                # 条件に一致するファイルをダウンロード
                for file in files:
                    if date in file and band in file:
                        local_path = os.path.join(LOCAL_DIR, file)
                        if not os.path.exists(local_path):  # 重複ダウンロードを防止
                            with open(local_path, "wb") as f:
                                ftp.retrbinary(f"RETR {file}", f.write)
                            print(f"Downloaded: {file}")
                        else:
                            print(f"Already exists: {file}")

# 使用例
dates = ["20241115", "20241116"]  # 複数の日付を指定
bands = ["B03", "B08"]  # 複数バンドを指定
download_files(dates, bands)

print("Download completed.")
