#!/bin/bash
tar -c ./tmp/pycharm/ | xz -9 -T0 -v > ./tmp/pycharm.tar.xz
exec bash
