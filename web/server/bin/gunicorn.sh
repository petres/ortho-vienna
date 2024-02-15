#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

. ./venv/bin/activate
gunicorn -w 2 "api:create_app()" -b 127.0.0.1:9888

