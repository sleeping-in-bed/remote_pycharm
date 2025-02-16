#!/bin/bash
python3 .compose/compose.py -e BASE_IMAGE=paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6 "$@"
docker build -f ./Dockerfile -t paddle_dev ..
exec bash
