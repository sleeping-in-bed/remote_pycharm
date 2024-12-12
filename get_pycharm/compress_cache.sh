#!/bin/bash
tar -c -C tmp pycharm | xz -9 -T0 -ve > ./tmp/pycharm.tar.xz
exec bash
