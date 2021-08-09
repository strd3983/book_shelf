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
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find('table', {'class': 'wikitable'}).tbody
    rows = table.find_all('tr')
    columns = [v.text.replace('\n', '') for v in rows[0].find_all('th')]
    for i in range(len(rows)):
        # 全ての<td>タグ（セルデータ）を取得しtdsに格納、リスト化
        tds = rows[i].find_all('td')
        if len(tds) == len(columns):
            # （ある行成分の）全セルデータをテキスト成分としてvaluesに格納、リスト化
            values = [
                td.text.replace('\n', '').replace('\xa0', ' ') for td in tds
            ]
            print(values)


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
    # title = soup.select_one('#firstHeading').getText()
    table = soup.find('table', {'class': 'infobox bordered'}).tbody
    rows = table.find_all('tr')
    info = []
    info.append(['タイトル', rows[0].getText().replace('\n', '')])
    for i in range(len(rows)):
        ths = rows[i].find_all('th')
        if len(ths) == 1:
            index = [
                th.text.replace('\n', '').replace('\xa0', ' ') for th in ths
            ]
            tds = rows[i].find_all('td')
            if len(tds) == 1:
                data = [
                    td.text.replace('\n', '').replace('\xa0', ' ')
                    for td in tds
                ]
                info.append(index + data)
    return info


if __name__ == "__main__":
    main()
    print('終了しました')
    os.system('PAUSE')
