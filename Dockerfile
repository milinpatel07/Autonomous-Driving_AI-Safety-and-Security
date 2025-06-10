FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-devel

ENV TORCH_CUDA_ARCH_LIST="7.5" \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential git nano libgl1 ffmpeg libsm6 libxext6 make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/OpenPCDet_Car
COPY . /workspace/OpenPCDet_Car

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    pip3 install spconv-cu121 ensemble-boxes

RUN git config --global --add safe.directory /workspace/OpenPCDet_Car

RUN python3 setup.py develop

CMD ["bash"]
