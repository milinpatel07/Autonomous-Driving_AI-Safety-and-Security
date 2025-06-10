FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

WORKDIR /workspace/OpenPCDet
COPY . /workspace/OpenPCDet

RUN pip install -r requirements.txt \
    && pip install spconv-cuda12.1 ensemble-boxes \
    && python setup.py develop

CMD ["bash"]
