FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    r-base \
    r-cran-randomforest \
    python3.7 \
    python3-pip \
    python3-setuptools \
    python3-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY packages.R /app/packages.R

RUN pip3 install -r requirements.txt

RUN Rscript packages.R

# needed?
# COPY . /app
