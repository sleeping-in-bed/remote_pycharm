#!/bin/bash
source .env
docker push "wantodie/build-data:$TAG"
exec bash
