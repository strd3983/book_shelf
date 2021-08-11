# book_shelf - 既刊情報の取得
## ソフトウェアの概要
既刊情報と自分の既読情報を羅列するPythonプログラム。同階層に**"setting.ini"** を作成し以下を記述する。
- [DEFAULT]
  - number: 検索する本の冊数
- [1]
  - URL: AmazonのコレクションID
  - Read: 既読した巻数
- [2] 
  - URL: AmazonのコレクションID
  - Read: 既読した巻数
- 以下同様にnumberまで

ただし以下の「[ダウンロード](#ダウンロード)」に示したファイルをDLする必要がある。

## ビルドについて
### ダウンロード
ビルド時に次の二つが必要になる。
1. ドライバ: [chrome-driver](https://chromedriver.chromium.org/downloads)
2. ブラウザ: [chronium](https://www.chromium.org/getting-involved/download-chromium)

これらは **book_shelf.py** と同じ階層にて、1.については **\bin** フォルダ下に、2.については **\browser** フォルダ下に配置する必要がある。

### PyInstallerによってアプリケーション化
PyInstallerを用いてPowerShell等で以下のコマンドによりexe化できる。(ファイルサイズはとても大きくなる)
```ps1:github.ps1
pyinstaller.exe .\book_shelf.py -F --add-binary ".\bin\chromedriver.exe;.\bin" --add-data ".\browser;.\browser"
```
