#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR

mkdir appdata

# API
# docker stop upload_api_inst
# docker rm upload_api_inst


docker-compose up -d