FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    r-base \
    python3.7 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    cmake \
    libcurl4-openssl-dev \
    libssl-dev \
    libgsl0-dev \
    libeigen3-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libcairo2-dev \
    libxt-dev \
    libgtk2.0-dev \
    libcairo2-dev \
    xvfb  \
    xauth \
    xfonts-base \
    libz-dev \
    libhdf5-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY packages.R /app/packages.R

RUN pip3 install -r requirements.txt

RUN Rscript packages.R

ENTRYPOINT ["/run_benchmark.py"]