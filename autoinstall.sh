#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR

mkdir -p appdata
mkdir -p logs

# Generate ENV:

cp "$DIR/env_example" "$DIR/.env"

cd $DIR
docker-compose up -d --build