#!/bin/bash
python3 .compose/compose.py -e BASE_IMAGE=pytorch/pytorch:2.2.2-cuda11.8-cudnn8-devel "$@"
docker build -f ./Dockerfile -t pytorch_dev ..
exec bash
