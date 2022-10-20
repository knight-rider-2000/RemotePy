import grpc
from proto import remotepy_pb2
from proto import remotepy_pb2_grpc
from google.protobuf import empty_pb2
from datetime import datetime


def exemple():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = remotepy_pb2_grpc.RemotePyStub(channel)

        print("1. python version service")
        print("2. python pip freeze")
        print("3. new venv")
        print("4. pip install")
        print("5. delete venv")
        print("6. pip uinstall")
        print("7. list venv")
        print("8. Exec python -c")

        tmp_idVenv = ""

        while True:
            rpc_call = input("Which rpc would you like to test: ")

            if rpc_call == "1":
                request = remotepy_pb2.VersionRequest(idVenv=tmp_idVenv)
                replay = stub.Version(request)
                print(replay.version)
            elif rpc_call == "2":
                request = remotepy_pb2.PackagesRequest(idVenv=tmp_idVenv)
                replay = stub.Packages(request)
                print(replay.packages)
            elif rpc_call == "3":
                request = remotepy_pb2.NewVenvRequest(pythonVersion="python3")
                replay = stub.NewVenv(request)
                print(replay.idVenv)
                tmp_idVenv = replay.idVenv
            elif rpc_call == "4":
                request = remotepy_pb2.PipInstallRequest(idVenv=tmp_idVenv, package="Flask==2.2.2")
                stub.PipInstall(request)
            elif rpc_call == "5":
                request = remotepy_pb2.DeleteVenvRequest(idVenv=tmp_idVenv)
                stub.DeleteVenv(request)
            elif rpc_call == "6":
                request = remotepy_pb2.PipUninstallRequest(idVenv=tmp_idVenv, package="click==8.1.3,Flask==2.2.2,importlib-metadata==5.0.0,itsdangerous==2.1.2,Jinja2==3.1.2,MarkupSafe==2.1.1,Werkzeug==2.2.2")
                stub.PipUninstall(request)
            elif rpc_call == "7":
                replay = stub.ListVenv(empty_pb2.Empty())
                print(replay.list)
            elif rpc_call == "8":
                code = "import time\nfor i in range(3):\n\tprint(i)\n\ttime.sleep(1)\nERRROOR"
                request = remotepy_pb2.ExecRequest(idVenv=tmp_idVenv, code=code)
                replies = stub.Exec(request)
                for reply in replies:
                    if reply.type == remotepy_pb2.Std.STDOUT:
                        print("[STDOUT:{date}] {log}".format(date=datetime.fromtimestamp(reply.timestamp),
                                                             log=reply.log), end='')
                    elif reply.type == remotepy_pb2.Std.STDERR:
                        print("[STDERR:{date}] {log}".format(date=datetime.fromtimestamp(reply.timestamp),
                                                             log=reply.log), end='')


if __name__ == "__main__":
    exemple()
