#!/bin/bash
mkdir -p ./tmp

# copy from the container
copy_dir() {
    local dir_name="$1"
    local dest_dir="./tmp/data/${dir_name}"
    mkdir -p "${dest_dir}"
    parent_dir=$(dirname "$dest_dir")
    docker compose cp "$SERVICE:/home/a/${dir_name}" "${parent_dir}"
}

copy_dir ".cache/JetBrains"
copy_dir ".local/share/JetBrains"
copy_dir ".config/JetBrains"
copy_dir ".java"
copy_dir ".vscode-server"
copy_dir ".dotnet"

# compress
SRC_PATH=./tmp/data.tar.xz
DST_PATH=../build-data/data.tar.xz
tar -c -C tmp data | xz -9 -T0 -ve > ${SRC_PATH}
mv $SRC_PATH $DST_PATH

exec bash
