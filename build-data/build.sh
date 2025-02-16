#!/bin/bash
source .env
docker build -t "wantodie/build-data:$TAG" .
exec bash
