FROM cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.1-tf2.3.0:latest

USER root
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    cmake \
    gfortran \
    libgeos-dev \
    libproj-dev \
    proj-bin \
    proj-data  \
    wget

RUN pip3 install cmake --upgrade

RUN wget https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.22.1-Source.tar.gz \
    && tar -xzf eccodes-2.22.1-Source.tar.gz \
    && mkdir build ; cd build ; cmake -DCMAKE_INSTALL_PREFIX=/usr ../eccodes-2.22.1-Source \
    && cd /app/build ; make -s -j 4; ctest ; make install

COPY requirements.txt .
RUN pip install -r requirements.txt && python3 -m cfgrib selfcheck

USER user