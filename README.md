# Benchmark

## Usage

This repository defines a docker environment that contains R and Python kernels with the dependencies required to
run the benchmarking scripts. R dependencies are installed by `packages.R` and python dependencies are listed in
`requirements.txt`

## Build Docker

Install [Docker](https://docs.docker.com/v17.09/engine/installation/). Run, from the root of the repository:

`> docker build -t normjam -f Dockerfile .`

## Use container

When docker is installed on your system, the following command will drop you into a bash shell that exposes R & python
installed.

`> docker run -it normjam`
