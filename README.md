# Photo Metadata Updater with JSON
Googleフォトからダウンロードした画像の撮影日時を、
添付されるメタデータに基づき修正するスクリプト。

# How to use
`data/` にjpgとJSONのペアを置くだけです。
再帰的に走査するので、フォルダ階層はいくつでも問題ありませんが、
jpgとJSONは同じ階層に置かれていることが前提です。

引数を与える形にしておけばよかったです。
