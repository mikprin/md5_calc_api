#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR

mkdir appdata

# Generate ENV:

cp "$DIR/env_example" "$DIR/.env"

docker-compose up -d