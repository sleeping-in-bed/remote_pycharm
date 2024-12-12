#!/bin/bash
source .env
python3 compose.py -e BASE_IMAGE=pytorch/pytorch:2.2.2-cuda11.8-cudnn8-devel "$@"
docker build -t pytorch_pycharm .
exec bash
