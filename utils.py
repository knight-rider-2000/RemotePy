"""
Contains function to simplify requests to the server
"""

from proto import remotepy_pb2
from google.protobuf import empty_pb2


def version(stub, id_venv):
    request = remotepy_pb2.VersionRequest(idVenv=id_venv)
    replay = stub.Version(request)
    return replay.version


def package(stub, id_venv):
    request = remotepy_pb2.PackagesRequest(idVenv=id_venv)
    replay = stub.Packages(request)
    return replay.packages


def pip_install(stub, id_venv, packages):
    request = remotepy_pb2.PipInstallRequest(idVenv=id_venv,
                                             package=packages)
    stub.PipInstall(request)


def delete_venv(stub, id_venv):
    request = remotepy_pb2.DeleteVenvRequest(idVenv=id_venv)
    stub.DeleteVenv(request)


def pip_uninstall(stub, id_venv, packages):
    request = remotepy_pb2.PipUninstallRequest(idVenv=id_venv,
                                               package=packages)
    stub.PipUninstall(request)


def list_venv(stub):
    replay = stub.ListVenv(empty_pb2.Empty())
    return replay.list


def exec_python(stub, id_venv, code):
    request = remotepy_pb2.ExecRequest(idVenv=id_venv,
                                       code=code)
    replies = stub.Exec(request)
    return replies


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