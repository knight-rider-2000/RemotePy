import os
import grpc
import time
import queue
import shutil
import subprocess
import configparser
from uuid import uuid1
from threading import Thread
from datetime import datetime
from concurrent import futures
from proto import remotepy_pb2
from proto import remotepy_pb2_grpc
from google.protobuf import empty_pb2


class RemotePyServer(remotepy_pb2_grpc.RemotePyServicer):
    """
    Remote python service class

    Attributes
    ----------


    Methods
    -------
    Version(request, context)
        Return python version
    Packages(request, context)
        Return package list
    PipInstall(request, context)
        Install new package on given virtualenv
    NewVenv(request, context)
        Create new virtualenv
    DeleteVenv(request, context)
        Delete existing virtualenv
    PipUninstall(request, context)
        Uninstall packages
    ListVenv(request, context)
        Return list of existing virtualenv
    Exec(request, context)
        Execute python code
    is_venv(id_venv)
        Check if virtualenv exit

    Raises
    ------
    """
    def Version(self, request, context):
        """
        Return python version for a given virtualenv

        Parameters
        ----------
        request.idVenv : String (UUID)
            Id virtualenv.

        Returns
        -------
        String
            replay.version: python version.
        """

        self.check_venv(request.idVenv)
        python_cmd = f"{CONFIG['virtualenv']['virtualenvs_path']}{request.idVenv}/bin/python"
        proc = subprocess.Popen([python_cmd, "-c", "import sys; print(sys.version)"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        replay = remotepy_pb2.VersionReply()
        replay.version = proc.stdout.read().decode("utf8")
        return replay

    def Packages(self, request, context):
        """
        Return installed packages for a given virtualenv

        Parameters
        ----------
        request.idVenv : String (UUID)
            Id virtualenv.

        Returns
        -------
        String
            replay.packages: package list.
        """
        self.check_venv(request.idVenv)
        pip_cmd = f"{CONFIG['virtualenv']['virtualenvs_path']}{request.idVenv}/bin/pip"
        proc = subprocess.Popen([pip_cmd, "freeze"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        replay = remotepy_pb2.PackagesReply()
        replay.packages = proc.stdout.read().decode("utf8")

        return replay

    def PipInstall(self, request, context):

        self.check_venv(request.idVenv)
        pip_cmd = f"{CONFIG['virtualenv']['virtualenvs_path']}{request.idVenv}/bin/pip"
        packages = str(request.package).replace('"', '').split(",")
        for package in packages:
            proc = subprocess.Popen([pip_cmd, "install", package],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        return empty_pb2.Empty()

    def NewVenv(self, request, context):

        id = str(uuid1())
        venvPath = f"{CONFIG['virtualenv']['virtualenvs_path']}{id}"
        # Select python version
        if str(request.pythonVersion).lower() == "python3":
            python_path = CONFIG['virtualenv']['python3_path']
        else:
            python_path = CONFIG['virtualenv']['python_path']

        proc = subprocess.Popen([python_path, "-m", "venv", venvPath],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        replay = remotepy_pb2.NewVenvReply()
        replay.idVenv = id

        time.sleep(0.1)
        if not self.is_venv(id):
            raise Exception(f"Internal error has occurred !")

        return replay

    def DeleteVenv(self, request, context):

        self.check_venv(request.idVenv)
        venv_dir = f"{CONFIG['virtualenv']['virtualenvs_path']}{request.idVenv}"
        shutil.rmtree(venv_dir)

        return empty_pb2.Empty()

    def PipUninstall(self, request, context):

        self.check_venv(request.idVenv)
        pip_cmd = f"{CONFIG['virtualenv']['virtualenvs_path']}{request.idVenv}/bin/pip"
        packages = str(request.package).replace('"', '').split(",")

        for package in packages:
            proc = subprocess.Popen([pip_cmd, "uninstall", "-y", package],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        return empty_pb2.Empty()

    def ListVenv(self, request, context):

        venvs_path = f"{CONFIG['virtualenv']['virtualenvs_path']}"
        list = []

        if os.path.exists(venvs_path):
            files = os.listdir(venvs_path)

            for tmp_file in files:
                if os.path.isdir(f"{venvs_path}/{tmp_file}"):
                    list.append(tmp_file)
        replay = remotepy_pb2.ListVenvReply()
        replay.list = ','.join(list)

        return replay

    def Exec(self, request, context):
        """Execute python code in a given environment
        This function receives a code in string
        forma and execute it with a python -c on the
        chosen environment and returns the output
        stdout, stderr.

        :param request.idVenv: Id virtualenv
        :type request.idVenv: String (UUID)
        :param request.code : Python code to execute
        :type request.code : String

        :return: Reply iterator continent log, type, timestamp.
        :rtype: Iterator
        """

        self.check_venv(request.idVenv)

        def out_reader(proc, log_queue):
            for line in iter(proc.stdout.readline, b''):
                log_queue.put((remotepy_pb2.Std.STDOUT, line.decode("utf8")))
            log_queue.put((remotepy_pb2.Std.STDOUT,"end"))

        def err_reader(proc, log_queue):
            for line in iter(proc.stderr.readline, b''):
                log_queue.put((remotepy_pb2.Std.STDERR, line.decode("utf8")))
            log_queue.put((remotepy_pb2.Std.STDERR,"end"))

        python_cmd = f"{CONFIG['virtualenv']['virtualenvs_path']}{request.idVenv}/bin/python"
        log_queue = queue.Queue()
        proc = subprocess.Popen([python_cmd, "-c", request.code],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        th_out = Thread(target=out_reader, args=(proc, log_queue,))
        th_err = Thread(target=err_reader, args=(proc, log_queue,))
        th_out.daemon = False
        th_err.daemon = False
        th_out.start()
        th_err.start()

        while True:
            reply = remotepy_pb2.ExecReply()
            reply.type, reply.log = log_queue.get()
            reply.timestamp = int(round(datetime.now().timestamp()))

            if proc.poll() is not None:
                break
            yield reply
            log_queue.task_done()

        th_out.join()
        th_err.join()

    def is_venv(self, id_venv):
        """
        Check if virtualenv with id_venv exist

        This function check if exist directory
        in virtualenv directory if there are directory
        named with id_venv.

        Parameters
        ----------
        id_venv : String (UUID)
            Id virtualenv.

        Returns
        -------
        Boolean
            True if virtualenv exit False otherwise.
        """
        return str(id_venv).strip() != '' and \
               os.path.exists(f"{CONFIG['virtualenv']['virtualenvs_path']}{id_venv}")

    def check_venv(self, id_venv):
        """
        Raise exception if given virtualenv don't exit

        Parameters
        ----------
        id_venv : String (UUID)
            Id virtualenv.

        Returns
        -------
            None
        """
        if not self.is_venv(id_venv):
            raise Exception(f"Don't find virtualenv with id : {id_venv} !")


def start_server(host, port, num_workers=3):
    """
    Start new server

    Parameters
    ----------
    host : String
        Server ip address to use.
    port : String
        Server port to use.
    num_workers: String
        Number of worker to launch by server.

    Returns
    -------
        None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=num_workers))
    remotepy_pb2_grpc.add_RemotePyServicer_to_server(RemotePyServer(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()


def config_file_path():
    """
    Return config file path from comfig directory (./confi)

    Parameters
    ----------
    host : String
        Server ip address to use.
    port : String
        Server port to use.
    num_workers: String
        Number of worker to launch by server.

    Returns
    -------
        @return : Config file path

    """

    current_file = os.path.dirname(__file__)
    config_dire = os.path.normpath(current_file + "/config")
    config_files = os.listdir(config_dire)

    # Keep first file with extension .ini
    config_file = ""
    for file in config_files:
        if file.endswith(".ini"):
            return f"{config_dire}/{file}"


if __name__ == "__main__":

    # Load file config
    CONFIG = configparser.ConfigParser()
    CONFIG.read(config_file_path())

    # Start server
    start_server(host=CONFIG['server']['host'],
                 port=CONFIG['server']['port'],
                 num_workers=int(CONFIG['server']['num_workers']))



