import os
import requests
import configparser
from bs4 import BeautifulSoup

# import pandas as pd


# --------------------------------------------------
# メイン関数
# --------------------------------------------------
def main():
    url = config()
    if url == 0:
        return


# --------------------------------------------------
# 設定iniファイルの読み込み
# --------------------------------------------------
def config():
    config_ini = configparser.ConfigParser(interpolation=None)
    config_ini_path = 'setting.ini'
    # iniファイルが存在するかチェック
    if os.path.exists(config_ini_path):
        # iniファイルが存在する場合、ファイルを読み込む
        with open(config_ini_path, encoding='utf-8') as fp:
            config_ini.read_file(fp)
            # iniの値取得
            read_default = config_ini['DEFAULT']
            url = read_default.get('URL', raw=True)
            # 設定出力
            info = book_info(url)
            print('#########################################')
            for i in range(len(info)):
                if info[i][0] == 'タイトル':
                    print('書籍名:', info[i][1])
                if info[i][0] == '著者':
                    print('著者名:', info[i][1])
            print('#########################################')
            return url
    else:
        print('setting.iniが見つかりません\n')
        return 0


# --------------------------------------------------
# 書籍情報の取得
# --------------------------------------------------
def book_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.select_one('#collection-title')
    print(title)
    info = []
    info.append(['タイトル', title])
    return info


if __name__ == "__main__":
    main()
    print('終了しました')
    os.system('PAUSE')
