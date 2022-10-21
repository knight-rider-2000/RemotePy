# RemotePy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Table of contents**

- [Description](#Description)
- [Requirement](#Requirement)
- [Getting started](#Getting-started)
- [Configuration](#Configuration)

## Description

RemotePy allow you to manage python virtualenv remotely as well as execute python code remotly. 
It composed by server and client side which use gRPC framework to communicate 

## Requirement
- Python 3.8
- Pip 
- Virtualenv
- Linux (tested on ubuntu)

## Getting started
### Start service
```shell
$ python ./server.py
```
### Execute client exemple



### Configuration

### Generate proto
If you want to regenerate proto file you need the following instructions :
``` bash
# Update pip
pip install --upgrade pip
# Install grpcio and grpcio-tools packages
pip install grpcio
pip install grpcio-tools
# Generate pb2 files from proto file
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. proto/remotepy.proto
```

