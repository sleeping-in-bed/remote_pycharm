#!/bin/bash
source .env
python3 compose.py -e BASE_IMAGE=python:3.10 "$@"
docker build -t remote_pycharm .
exec bash
