import os
import requests
import configparser
from bs4 import BeautifulSoup as bs4

# import pandas as pd


# --------------------------------------------------
# メイン関数
# --------------------------------------------------
def main():
    urls = config()
    if urls == 0:
        return
    for url in urls:
        book_info(url)


# --------------------------------------------------
# 設定iniファイルの読み込み
# --------------------------------------------------
def config():
    config_ini = configparser.ConfigParser(interpolation=None)
    config_ini_path = 'setting.ini'
    urls = []
    # iniファイルが存在するかチェック
    if os.path.exists(config_ini_path):
        # iniファイルが存在する場合、ファイルを読み込む
        with open(config_ini_path, encoding='utf-8') as fp:
            config_ini.read_file(fp)
            # iniの値取得
            for i in range(1, int(config_ini['DEFAULT']['number']) + 1):
                url = config_ini[str(i)]['URL']
                urls.extend(['https://www.amazon.co.jp/gp/product/' + url])
            # 設定出力
            return urls
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

    # シリーズ情報の取得
    title = soup.find('title').get_text(strip=True).replace('Kindle版', '')
    author = soup.find('span', {'id': 'author-name'}).get_text(strip=True)
    print('\n#############################################################')
    print('シリーズ名:', title)
    print('著者名:', author)
    print('URL:', url)
    print()

    # 既刊情報の取得
    titles = soup.find_all(
        'a',
        {'class': 'a-size-base-plus a-link-normal itemBookTitle a-text-bold'})
    for i, title in enumerate(titles):
        print(i, ':', title.get_text(strip=True))
    print('#############################################################\n')
    return


if __name__ == "__main__":
    main()
    # print('終了しました')
    # os.system('PAUSE')
