from psplpy import DynamicCompose
dc = DynamicCompose()

base_image = dc.env['BASE_IMAGE']
if base_image in ['python:3.10']:
    dc.env['SOMETHING_ELSE'] = 'apt install -y --no-install-recommends firefox-esr'
elif base_image in ['pytorch/pytorch:2.2.2-cuda11.8-cudnn8-devel']:
    dc.env['SOMETHING_ELSE'] = 'conda install -y jupyter'
elif base_image in ['paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6']:
    dc.env['SOMETHING_ELSE'] = ('pip install paddleocr && '
    				'python -c "import paddle; import paddleocr; paddleocr.PaddleOCR(use_gpu=False)"')
else:
    raise ValueError()

dc.fd_dockerfile()

