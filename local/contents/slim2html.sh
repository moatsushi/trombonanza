# slim to html

outputdir='../../../org.trombonanza.hedgehog'

cd slim

mkdir ${outputdir}

rm -rf mkdir ${outputdir}/archive
mkdir ${outputdir}/archive


for f in `find . -type f`
do
	filename=${f%.*}
	ext=${f##*.}
	if [ $ext = "slim" ] ; then
		plimc --html -o ${outputdir}/${filename}.html ${filename}.slim
	fi
done
