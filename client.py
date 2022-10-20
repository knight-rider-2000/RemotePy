import grpc
from proto import remotepy_pb2
from proto import remotepy_pb2_grpc
from google.protobuf import empty_pb2
from datetime import datetime


def exemple():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = remotepy_pb2_grpc.RemotePyStub(channel)

        while True:
            try:
                print("1. python version")
                print("2. pip freeze")
                print("3. new venv")
                print("4. pip install")
                print("5. delete venv")
                print("6. pip uinstall")
                print("7. list venv")
                print("8. Exec python code")
                rpc_call = input("Which rpc service would you like to test: ")

                if rpc_call == "1":
                    id_venv = select_venv(stub)
                    request = remotepy_pb2.VersionRequest(idVenv=id_venv)
                    replay = stub.Version(request)
                    print(replay.version)

                elif rpc_call == "2":
                    id_venv = select_venv(stub)
                    request = remotepy_pb2.PackagesRequest(idVenv=id_venv)
                    replay = stub.Packages(request)
                    print(replay.packages)

                elif rpc_call == "3":
                    create_venv(stub)

                elif rpc_call == "4":
                    id_venv = select_venv(stub)
                    packages = "Flask==2.2.2"
                    print("Install package:", packages)
                    request = remotepy_pb2.PipInstallRequest(idVenv=id_venv, package=packages)
                    stub.PipInstall(request)

                elif rpc_call == "5":
                    id_venv = select_venv(stub)
                    request = remotepy_pb2.DeleteVenvRequest(idVenv=id_venv)
                    stub.DeleteVenv(request)

                elif rpc_call == "6":
                    id_venv = select_venv(stub)
                    packages = "click==8.1.3,Flask==2.2.2,importlib-metadata==5.0.0,itsdangerous==2.1.2,Jinja2==3.1.2,MarkupSafe==2.1.1,Werkzeug==2.2.2"
                    print("Uninstall package:", packages)
                    request = remotepy_pb2.PipUninstallRequest(idVenv=id_venv, package=packages)
                    stub.PipUninstall(request)

                elif rpc_call == "7":
                    replay = stub.ListVenv(empty_pb2.Empty())
                    print("->", replay.list.replace(",", "\n-> "))

                elif rpc_call == "8":
                    id_venv = select_venv(stub)
                    code = "import time\nfor i in range(3):\n\tprint(i)\n\ttime.sleep(1)\nERRROOR"
                    print("----------PYTHON CODE------------")
                    print(code)
                    print("----------END CODE---------------")
                    request = remotepy_pb2.ExecRequest(idVenv=id_venv, code=code)
                    replies = stub.Exec(request)
                    for reply in replies:
                        if reply.type == remotepy_pb2.Std.STDOUT:
                            print("[STDOUT:{date}] {log}".format(date=datetime.fromtimestamp(reply.timestamp),
                                                                 log=reply.log), end='')
                        elif reply.type == remotepy_pb2.Std.STDERR:
                            print("[STDERR:{date}] {log}".format(date=datetime.fromtimestamp(reply.timestamp),
                                                                 log=reply.log), end='')
            except Exception as err:
                print(err)
            print()


def select_venv(stub):

    replay = stub.ListVenv(empty_pb2.Empty())
    if replay.list != '':
        ids_env = replay.list.split(',')
        print("Select your virtualenv: ")
        for num, id_env in enumerate(ids_env):
                print("->", num, ":", id_env)
        while True:
            choice = input()
            if 0 <= int(choice) < len(ids_env):
                return ids_env[int(choice)]
    else:
        print("No virtualenv find you need create one before")
        return create_venv(stub)


def create_venv(stub):

    print("Select python version you need for virtualenv:")
    print("-> 1: python3")
    print("-> 2: python2")
    python_version = ""
    while True:
        choice = input()
        if 1 <= int(choice) <= 2:
            if int(choice) == 1:
                python_version = "python3"
                break
            else:
                python_version = "python2"
                break

    request = remotepy_pb2.NewVenvRequest(pythonVersion=python_version)
    replay = stub.NewVenv(request)
    print(replay.idVenv)
    return replay.idVenv


if __name__ == "__main__":
    exemple()
