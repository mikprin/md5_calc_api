#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR
if  docker ps | grep upload_api ; then
    echo "Stopping container:"
    docker stop upload_api_test
    docker rm upload_api_test

else
    echo "No existing containers found"
fi

docker build -t upload_api .

docker run -d --name upload_api_test -p 8000:8000 --add-host host.docker.internal:host-gateway -v $(realpath src/saved_files):/code/api/saved_files upload_api