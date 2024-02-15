#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

. ../../venv/bin/activate
flask --app api --debug run -h 0.0.0.0 -p 8889
