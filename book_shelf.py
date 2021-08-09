import os
import requests
import configparser
from bs4 import BeautifulSoup as bs4

# import pandas as pd


# --------------------------------------------------
# メイン関数
# --------------------------------------------------
def main():
    url = config()
    if url == 0:
        return
    book_info(url)


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
            url = 'https://www.amazon.co.jp/gp/product/' + url
            # 設定出力
            return url
    else:
        print('setting.iniが見つかりません\n')
        return 0


# --------------------------------------------------
# 書籍情報の取得
# --------------------------------------------------
def book_info(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    soup = bs4(page.text, "html.parser")
    title = soup.find('title').get_text(strip=True).replace('Kindle版', '')
    author = soup.find('span', {'id': 'author-name'}).get_text(strip=True)
    print('#########################################')
    print('書籍名:', title)
    print('著者名:', author)
    print('URL:', url)
    print('#########################################')
    return


if __name__ == "__main__":
    main()
    # print('終了しました')
    # os.system('PAUSE')
