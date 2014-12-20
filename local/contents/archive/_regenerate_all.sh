#! /bin/sh

#
# ディレクトリ構成
# - html  ... 出力ファイル .html
# - mako_template  ... テンプレート 拡張子は.baseslim
# - slim  ... 拡張子は .slim
# - archive_csv  ... generation
#
# ./slim に置かれた*.slimをfindで一括変換して ./html に出力します。
# templateは *.slim と同じディレクトリに置かないと読めないようなので、各ディレクトリにコピーします。
#


mkdir ../slim/
mkdir ../slim/archive
# mkdir ../html
# mkdir ../html/archive

rm -r ../slim/archive/*
cp ../mako_template/* ../slim/archive



python3 createarchive.py concert.sqlite


# slim to html

# cd ../slim
# for f in `find . -type f`
# do
# 	filename=${f%.*}
# 	ext=${f##*.}
# 	if [ $ext = "slim" ] ; then
# 		plimc --html -o ../html/${filename}.html ${filename}.slim
# 	fi
# done
