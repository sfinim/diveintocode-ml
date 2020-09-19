# pdf_translator

### 概要
論文とか、英語で書かれたpdfファイルをgoogle翻訳で日本語に翻訳するツール。

### ディレクトリ構成
以下のディレクトリ構成で使用すること

pdf_translator
　├ pdf/
　├ en/
　├ ja/
　└ translate.py

各ディレクトリに格納されるファイルは以下の通り。
- pdf:翻訳したいpdfファイル
- en :翻訳前(英語)のテキストファイル(つまり、pdfをテキストファイルに変えただけのファイル)
- ja :翻訳後(日本語)のテキストファイル

### 使い方
翻訳したいpdfファイルを"pdf"ディレクトリに格納して以下を実行。
`> python translate.py`

- "en","ja"ディレクトリにpdfに対応したファイルが生成される。
- 複数pdfファイルがある場合はまとめて処理される。
- 変換済みのファイルがあるpdfファイルは処理をスキップする。

### pythonista3
iOSのpython実行環境である"pythonista3"においても動作確認済。

#### pythonista3をインストール
https://apps.apple.com/jp/app/pythonista-3/id1085978097

#### pythonista3でpipを使えるようにする
https://nikukyulog.com/programming/python/install-stash-on-pythonista3/

#### pipで必要パッケージをインストール
- pip install requests
- pip install pdfminer.six
- pip install googletrans

論文などのpdfをダウンロードしてtranslate.pyを実行すれば動きます。
