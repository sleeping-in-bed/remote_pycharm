#!/bin/bash
python3 .compose/compose.py -e BASE_IMAGE=buildpack-deps:bookworm "$@"
docker build -f ./Dockerfile -t container_dev ..
exec bash
