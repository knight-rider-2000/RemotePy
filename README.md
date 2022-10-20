
### Needed for gRPC
``` bash
python -m pip install --upgrade pip
pip install --upgrade pip
pip install grpcio
pip install grpcio-tools
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. proto/remotepy.proto
```

### Python version 
```
python3.8.10
```