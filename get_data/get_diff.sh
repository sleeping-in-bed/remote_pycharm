#!/bin/bash
mkdir -p ./tmp
docker diff get_pycharm-get_pycharm-1 > ./tmp/diff.txt
exec bash
