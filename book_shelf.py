import os
import sys
import time
import configparser
from bs4 import BeautifulSoup as bs4
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

# Seleniumにて用いる待機時間
WAIT = 1


# --------------------------------------------------
# メイン関数
# --------------------------------------------------
def main():
    urls, rnums = config()
    if urls == 0:
        return
    for i in range(len(urls)):
        # URLが不確かなものは除外
        if len(str(urls[i])) == 51 + 10:
            book_info(urls[i], rnums[i])


# --------------------------------------------------
# 設定iniファイルの読み込み
# --------------------------------------------------
def config():
    config_ini = configparser.ConfigParser(interpolation=None)
    config_ini_path = rel2abs_path('setting.ini', 'exe')
    urls = []  # URLの集合
    rnums = []  # 既読数の集合
    # iniファイルが存在するかチェック
    if os.path.exists(config_ini_path):
        # iniファイルが存在する場合、ファイルを読み込む
        with open(config_ini_path, encoding='utf-8') as fp:
            config_ini.read_file(fp)
            # iniの値取得
            for i in range(int(config_ini['DEFAULT']['number'])):
                url, rnum = 0, 0  # 読み取り不可時のために0で初期化
                try:
                    url = config_ini[str(i + 1)]['URL']
                    url = f'https://www.amazon.co.jp/gp/product/{url}?language=ja_JP'
                except Exception:
                    print(f'W: [{str(i + 1)}]のURLが不明です')

                try:
                    rnum = config_ini[str(i + 1)]['Read']
                except Exception:
                    print(f'W: [{str(i + 1)}]の既読数が不明です')
                urls.extend([url])
                rnums.extend([rnum])
            print()
            return urls, rnums
    else:
        print('E: setting.iniが見つかりません')
        return 0, 0


# --------------------------------------------------
# 書籍情報の取得
# --------------------------------------------------
def book_info(url, rnum):
    try:
        page = get_html(url)
    except Exception as e:
        print('E: get_htmlでエラー')
        print(e)
        page = 0
    if page == 0:
        return
    soup = bs4(page, 'html5lib')

    # シリーズ情報の取得
    title = soup.find('title').get_text(strip=True).replace('Kindle版', '')
    author = soup.find('span', {'id': 'author-name'}).get_text(strip=True)
    print('\n#############################################################')
    print(f'シリーズ名: {title}')
    print(f'著者名: {author}')
    print('URL:', url.replace('?language=ja_JP', ''))
    print()

    # 既刊情報の取得
    titles = soup.find_all(
        'a', {'class': 'a-size-base-plus a-link-normal itemBookTitle a-text-bold'})
    for i in range(len(titles)):
        if i == int(rnum):
            print('---------------------------以下未読---------------------------')
        print(f'{i + 1} : {titles[i].get_text(strip=True)}')
    print('#############################################################\n')
    return


# --------------------------------------------------
# 動的htmlをseleniumによって取得
# --------------------------------------------------
def get_html(url):
    # パスの設定
    browser_path = rel2abs_path(r'.\data\browser\chrome.exe', 'exe')
    driver_path = rel2abs_path(r'.\data\bin\chromedriver.exe', 'exe')

    # WebDriver のオプションを設定する
    options = webdriver.ChromeOptions()
    options.binary_location = browser_path
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # ドライバ設定
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.request_interceptor = interceptor

    # URLへの接続
    driver.get(url)
    driver.set_window_size(100, 200)
    try:
        i = 0
        while True:
            i += 1
            print(f'M: {i}頁目取得')
            find_tag = '//a[@class="a-link-normal" and @href="javascript:"]'
            elems = driver.find_elements(By.XPATH, find_tag)
            if elems == [] or elems[0].text != '続きを表示':
                break
            # show_all = elems[1]
            driver.execute_script('arguments[0].scrollIntoView();', elems[0])
            time.sleep(WAIT)
            elems[0].click()
            time.sleep(WAIT)
        html = driver.page_source.encode('utf-8')
        driver.quit()
        return html

    except Exception as e:
        print('E: Seleniumにてエラー発生')
        print(e)
        driver.quit()
        return 0


# --------------------------------------------------
# 絶対パスを相対パスに [入:相対パス, 実行ファイル側or展開フォルダ側 出:絶対パス]
# --------------------------------------------------
def rel2abs_path(filename, attr):
    if attr == 'temp':  # 展開先フォルダと同階層
        datadir = os.path.dirname(__file__)
    elif attr == 'exe':  # exeファイルと同階層の絶対パス
        datadir = os.path.dirname(sys.argv[0])
    else:
        raise print(f'E: 相対パスの引数ミス [{attr}]')
    return os.path.join(datadir, filename)


# --------------------------------------------------
# seleniumにて読み込まないものを指定
# --------------------------------------------------
def interceptor(request):
    BLOCK_URLS = [
        'pvtag.yahoo.co.jp',
        'b5.yahoo.co.jp',
        's.yjtag.jp',
        'yads_vimps.js',
        'logql.yahoo.co.jp',
    ]
    # 画像類をブロック
    if request.path.endswith(('.png', '.jpg', '.gif')):
        request.abort()
    # URLをブロック
    if any([request.url.find(bloc_url) != -1 for bloc_url in BLOCK_URLS]):
        request.abort()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('E: ', e)
    print('終了しました')
    os.system('PAUSE')
