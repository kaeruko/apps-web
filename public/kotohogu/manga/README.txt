ことほぎのまち・まんが掲載メモ

新しい画像をこの manga フォルダへ追加してください。
1枚の画像は1作品として掲載されます。
例：manga/02_とんこのお茶.png

複数ページの作品はフォルダにまとめてください。
例：manga/とんこのお茶/01.png
　　manga/とんこのお茶/02.png
　　manga/とんこのお茶/03.png
ページ順はファイル名の数字順です。対応画像：png / jpg / jpeg / webp / gif / avif

作品名は画像ファイル名またはフォルダ名から自動で付けられます。
名前がランダムなファイルには titles.json で表示タイトルを設定してください。
例： "file:ランダムなファイル名.png": "とんこのお茶"
フォルダなら："folder:とんこのお茶": "とんこのお茶（前編）"

追加・変更したあとは、サイトをデプロイしてください。
deploy.ps1 / deploy.sh が scripts/build_kotohogu_manga.py を実行し、
manga.html の掲載一覧を自動更新してからアップロードします。
ローカルでの一覧だけ先に更新する場合：
  python scripts/build_kotohogu_manga.py

公開予定URL：https://cloxs.jp/kotohogu/manga.html
