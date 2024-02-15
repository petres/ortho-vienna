#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`;
cd $BASE_FOLDER

# SET="svd.tar.gz"
SET="svd_vedai_dota.tar.gz"

echo 'Downloading ...'
wget https://vienna.abteil.org/data/unified/yolo-sets/${SET}
tar xzf ${SET}
