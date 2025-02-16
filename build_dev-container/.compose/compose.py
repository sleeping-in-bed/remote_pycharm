from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from get_dynamic_compose import get_dc

dc = get_dc()
base_image = dc.env['BASE_IMAGE']
dc.env['COPY'] = ''
for relpath in ['.cache/JetBrains',
                '.local/share/JetBrains',
                '.config/JetBrains',
                '.java',
                '.vscode-server',
                '.dotnet']:
    dc.env['COPY'] += f'COPY --from=extract --chown=${{USER_NAME}}:${{USER_NAME}} ${{BUILD_DATA_PATH}}/{relpath} ${{HOME}}/{relpath}\n'

dc.env['OTHER_BUILD_PROCESS'] = ''
if base_image in ['buildpack-deps:bookworm']:
    base_dir = Path(__file__).parent
    dc.env['OTHER_BUILD_PROCESS'] += (base_dir / 'node-20.18.3').read_text(encoding='utf-8')
    dc.env['OTHER_BUILD_PROCESS'] += (base_dir / 'python-3.10.16').read_text(encoding='utf-8')
    dc.env['SOMETHING_ELSE'] = """apt install -y --no-install-recommends firefox-esr &&\\
    # install common python packages
    pip install --no-cache-dir pyyaml aiohttp requests django "fastapi[all]" pyautogui pynput \\
    opencv-python opencv-python-headless "pillow<=9.5.0" "numpy<=1.26.4" selenium redis psycopg2-binary
"""
elif base_image in ['pytorch/pytorch:2.2.2-cuda11.8-cudnn8-devel']:
    dc.env['SOMETHING_ELSE'] = 'conda install -y jupyter'
elif base_image in ['paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6']:
    dc.env['SOMETHING_ELSE'] = """pip install paddleocr &&\\
    python -c "import paddle; import paddleocr; paddleocr.PaddleOCR(use_gpu=False)"
"""
else:
    raise ValueError()

dc.fd_dockerfile()
