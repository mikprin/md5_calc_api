#!/usr/bin/env bash
# DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# cd $DIR
docker stop upload_api_inst
docker rm upload_api_inst
