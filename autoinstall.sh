#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR

mkdir app_data

# API
# docker stop upload_api_inst
# docker rm upload_api_inst

docker build -t upload_api .

docker run -d --name upload_api_inst -p 8000:8000 --add-host host.docker.internal:host-gateway upload_api