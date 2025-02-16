#!/usr/bin/env python3
from dotenv import load_dotenv
import os
from pathlib import Path
import subprocess

load_dotenv()
SERVICE = os.environ.get('SERVICE')

SEARCH_PATH = Path('/home/a/.cache/JetBrains/RemoteDev/dist')
HOST_DEST = Path('./tmp')
HOST_DEST.mkdir(parents=True, exist_ok=True)
JETBRA_DIR = Path('./resources/jetbra')

DIR_NAMES = ("pycharm", "WebStorm")
VMOPTIONS_NAMES = ("pycharm64", "webstorm64")


def get_output(command: str) -> str:
    return subprocess.run(command, capture_output=True, text=True, shell=True).stdout


for dir_name, vmoptions_name in zip(DIR_NAMES, VMOPTIONS_NAMES):
    matching_dir = get_output(
        f'docker compose exec {SERVICE} find {SEARCH_PATH} -type d -name "*_{dir_name}-*"').strip()
    if not matching_dir:
        raise AssertionError

    bin_dir = Path(matching_dir) / 'bin'
    vmoptions_file = f'{vmoptions_name}.vmoptions'
    file_path = bin_dir / vmoptions_file
    dest_path = HOST_DEST / vmoptions_file
    os.system(f'docker compose cp "{SERVICE}:{file_path}" "{dest_path}"')
    jetbra_str = f"""
--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED
--add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED
-javaagent:{bin_dir}/jetbra/ja-netfilter.jar=jetbrains
"""
    content = dest_path.read_text(encoding='utf-8')
    if jetbra_str not in content:
        content += jetbra_str
        dest_path.write_text(content, encoding='utf-8')
        os.system(f'docker compose cp "{dest_path}" "{SERVICE}:{file_path}"')
        os.system(f'docker compose cp "{JETBRA_DIR}" "{SERVICE}:{bin_dir}"')
    else:
        print('Skip to add jetbra')

input('Finished\n')
