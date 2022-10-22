# RemotePy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Table of contents**

- [Description](#Description)
- [Requirement](#Requirement)
- [Getting started](#Getting-started)
- [Configuration](#Configuration)

## Description

RemotePy allow you to manage python virtualenv remotely as well as execute python code remotly. 
It composed by server and client side which use gRPC framework to communicate.

what you can do with RemotePy:
- Create/Delete/List virtualenv
- Install/Uninstall packages
- Execute python code on a virtualenv

## Requirement
- Python 3.8
- Pip 
- Virtualenv
- Linux (tested on ubuntu)

## Getting started
### Start server
```shell
$ python ./server.py
```
### Execute client example
You can find how to use different RemotePy services in ``.client.py``.

```shell
$ python ./client.py
```

### Configuration
You can find the file config file for service side in ``./config/prod.ini``.
#### Example file config
``` ini 
[server]
host = localhost    # Server address
port = 50051        # Server usage port
num_workers = 3     # Number of server workers 

[virtualenv]
virtualenvs_path = /tmp/virtualenvs/    # Virtualenv storage directory
python_path = /usr/bin/python           # Path to your system python2.7 
python3_path = /usr/bin/python3         # Path to your system python3

```

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

