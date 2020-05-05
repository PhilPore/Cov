#!/bin/bash

na=$1
linkarr=()
while read -r line
do
linkarr+=($line)
done < $na
echo "${linkarr[@]}"
echo ${linkarr[0]}
tagsoup="find tagsoup-1.2.1.jar"
if [ $(find tagsoup-1.2.1.jar) ]
then
echo "Tagsoup found!"
else
echo $(curl -o tagsoup-1.2.1.jar http://vrici.lojban.org/~cowan/XML/tagsoup/tagsoup-1.2.1.jar)
fi
while :
do
##http://vrici.lojban.org/~cowan/XML/tagsoup/tagsoup-1.2.1.jar
echo $(curl -o srce.html ${linkarr[0]})
echo $(java -jar tagsoup-1.2.1.jar --files srce.html)
python parser.py srce.xhtml
echo $(rm srce.html srce.xhtml)
echo "Done Parsing!"
sleep 30m
echo "Parsing!"
done 
