#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`;
cd $BASE_FOLDER

echo 'Uploading ...'
rsync -e 'ssh -p 23322' -Parv *.tar.gz petres@explorer100.abteil.org:/var/www/vienna/data/unified/yolo-sets
