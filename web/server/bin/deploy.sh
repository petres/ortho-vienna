#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER


rsync -e 'ssh -p 23322' -arv --exclude /instance --exclude '*/__pycache__/' ./ petres@explorer100.abteil.org:/var/www/vienna/server

rsync -e 'ssh -p 23322' -arv --exclude '*/__pycache__/' ../../utils/ petres@explorer100.abteil.org:/var/www/vienna/utils
rsync -e 'ssh -p 23322' -arv --delete --copy-links ../../data/model/ petres@explorer100.abteil.org:/var/www/vienna/data/model


# ssh -p 23322 petres@explorer100.abteil.org "/var/www/vienna/server/bin/venv.sh"
ssh -p 23322 petres@explorer100.abteil.org "sudo systemctl restart vienna-api-server"
