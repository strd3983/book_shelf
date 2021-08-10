import os
import sys
from seleniumwire import webdriver
from selenium.webdriver.common.by import By


# --------------------------------------------------
# 相対パス to 絶対パス
# --------------------------------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_html():
    # ブラウザ
    browser_path = resource_path('browser/chrome.exe')
    # ドライバ
    driver_path = resource_path('bin/chromedriver.exe')

    # WebDriver のオプションを設定する
    options = webdriver.ChromeOptions()
    options.binary_location = browser_path
    # options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # ドライバ設定
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.request_interceptor = interceptor

    # URLへの接続
    print('connectiong to remote browser...')
    driver.get('https://www.amazon.co.jp/-/jp/dp/B074BD9ZW8?language=ja_JP')
    driver.find_elements(By.XPATH, '//*[text()=\"全て表示\"]')
    driver.execute_script('window.scrollTo(0, " & element.Location.Y & ");')
    driver.find_elements(By.XPATH, '//*[text()=\"全て表示\"]').click
    # ブラウザを終了する
    driver.quit()


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


get_html()
