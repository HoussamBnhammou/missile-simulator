#!/bin/sh
set -eu

docker compose up -d
docker compose ps
