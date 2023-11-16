FROM nvidia/cuda:12.1.0-devel-ubuntu18.04

RUN apt-get update -q && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    vim \
    wget \
    xpra \
    supervisor \
    swig \
    xserver-xorg-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN DEBIAN_FRONTEND=noninteractive add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update -q
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y  \
    python3.8 \
    python3.8-dev  \
    python3.8-distutils \
    python3-pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
RUN update-alternatives --set python /usr/bin/python3.8
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN update-alternatives --set pip /usr/bin/pip3

RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade Pillow

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev

# RUN python -m ensurepip --upgrade

# RUN update-alternatives --set python /usr/bin/python3.6
# RUN update-alternatives --set pip /usr/bin/pip3.6

#RUN rm /usr/bin/python
#RUN ln -s /env/bin/python3.6 /usr/bin/python
#RUN ln -s /env/bin/pip3.6 /usr/bin/pip
#RUN ln -s /env/bin/pytest /usr/bin/pytest

RUN curl -o /usr/local/bin/patchelf https://s3-us-west-2.amazonaws.com/openai-sci-artifacts/manual-builds/patchelf_0.9_amd64.elf \
    && chmod +x /usr/local/bin/patchelf

ENV LANG C.UTF-8

RUN mkdir -p /root/.mujoco \
    && wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz \
    && tar -xf mujoco.tar.gz -C /root/.mujoco \
    && rm mujoco.tar.gz

ENV LD_LIBRARY_PATH /root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

COPY vendor/Xdummy /usr/local/bin/Xdummy
RUN chmod +x /usr/local/bin/Xdummy

# Workaround for https://bugs.launchpad.net/ubuntu/+source/nvidia-graphics-drivers-375/+bug/1674677
COPY ./vendor/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json

WORKDIR /mujoco_py
COPY ./requirements.txt /mujoco_py/
COPY ./requirements.dev.txt /mujoco_py/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.dev.txt

RUN pip install numpy scikit-learn==1.0.2 nvidia-cusolver-cu12==11.4.5.107 nvidia-curand-cu12==10.3.2.106
RUN pip install nvidia-cusparse-cu12==12.1.0.106 nvidia-cublas-cu12==12.1.3.1 nvidia-cudnn-cu12==8.9.2.26 triton==2.1.0
RUN pip install nvidia-nccl-cu12==2.18.1 nvidia-cufft-cu12==11.0.2.54 nvidia-nvjitlink-cu12 mpmath>=0.19 torch==2.1.0
RUN pip install gym==0.22.0 opencv-python==4.8.1.78 scipy==1.7.3 xgboost==1.7.1 cython==0.29.21 matplotlib==3.5.0
RUN pip install plotly==5.4.0 optuna==2.10.0 catboost==1.2 fastapi==0.92.0 websockets==10.4 fastparquet==2023.2.0
RUN pip install uvicorn==0.19.0 pydantic==1.10.12 requests==2.28.1 email-validator==2.0.0.post2 pymysql==1.1.0
RUN pip install cryptography==41.0.4 ale-py==0.7.5 Pillow opencv-python box2d-py==2.3.5 pybullet dm_control==1.0.9
RUN pip install pyqtgraph joblib==1.1.0 tqdm==4.66.1 pygame==2.5.2 setuptools==58.2.0 mujoco-py==2.1.2.14
RUN apt install -y patchelf
RUN python -c 'import mujoco_py'
COPY . /mujoco_py

# ENTRYPOINT ["/mujoco_py/vendor/Xdummy-entrypoint"]
# CMD ["pytest"]
# RUN #python setup.py install
