#!/bin/bash
source .env
mkdir -p ./tmp/pycharm/.cache
docker compose cp $SERVICE:/home/a/.cache/JetBrains ./tmp/pycharm/.cache/JetBrains
mkdir -p ./tmp/pycharm/.local/share
docker compose cp $SERVICE:/home/a/.local/share/JetBrains ./tmp/pycharm/.local/share/JetBrains
mkdir -p ./tmp/pycharm/.config
docker compose cp $SERVICE:/home/a/.config/JetBrains ./tmp/pycharm/.config/JetBrains
exec bash
