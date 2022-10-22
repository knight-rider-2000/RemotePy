import grpc
from proto import remotepy_pb2
from proto import remotepy_pb2_grpc
from datetime import datetime
import utils


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
                    id_venv = utils.select_venv(stub)
                    tmp_version = utils.version(stub, id_venv)
                    print(tmp_version)

                elif rpc_call == "2":
                    id_venv = utils.select_venv(stub)
                    tmp_package = utils.package(stub, id_venv)
                    print(tmp_package)

                elif rpc_call == "3":
                    utils.create_venv(stub)

                elif rpc_call == "4":
                    id_venv = utils.select_venv(stub)
                    packages = "Flask==2.2.2"
                    print("Install package:", packages)
                    utils.pip_install(stub, id_venv, packages)

                elif rpc_call == "5":
                    id_venv = utils.select_venv(stub)
                    utils.delete_venv(stub, id_venv)

                elif rpc_call == "6":
                    id_venv = utils.select_venv(stub)
                    packages = "click==8.1.3,Flask==2.2.2,importlib-metadata==5.0.0,itsdangerous==2.1.2," \
                               "Jinja2==3.1.2,MarkupSafe==2.1.1,Werkzeug==2.2.2 "
                    print("Uninstall package:", packages)
                    utils.pip_uninstall(stub, id_venv, packages)

                elif rpc_call == "7":
                    tmp_list_venv = utils.list_venv(stub)
                    print("->", tmp_list_venv.replace(",", "\n-> "))

                elif rpc_call == "8":
                    id_venv = utils.select_venv(stub)
                    code = "import time\nfor i in range(3):\n\tprint(i)\n\ttime.sleep(1)\nCAUSE_ERROR"
                    print("----------PYTHON CODE------------")
                    print(code)
                    print("----------END CODE---------------")
                    replies = utils.exec_python(stub, id_venv, code)
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


if __name__ == "__main__":
    exemple()
