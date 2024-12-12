#!/bin/bash

read -p "Please input tag, default 'latest': " TAG
if [ -z "$TAG" ]; then
    TAG="latest"
fi

docker push "wantodie/build-data:$TAG"
exec bash

