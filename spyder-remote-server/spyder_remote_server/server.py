# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

"""
Spyder remote server in charge of launching the zeroconf service and provide
a socket via ZMQ to provide spyder-kernels start/stop.
"""

import fnmatch
import json
import logging
import os
import platform
import pwd
import signal
import socket
import subprocess
import sys
import tempfile
import time

import zmq
from zeroconf import IPVersion, ServiceInfo, Zeroconf

from spyder_remote_server.conda_api import CondaManager
from spyder_remote_server.config import get_log_path, read_config
from spyder_remote_server.constants import SERVICE_TYPE
from spyder_remote_server.utils import find_free_port, get_ip, demote


# TODO: Check logging
logging.basicConfig(
    filename=get_log_path(),
    filemode="a",
    format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


class SpyderRemoteServer:
    """
    Spyder remote server in charge of launching the zeroconf service and provide
    a socket via ZMQ to provide spyder-kernels start/stop.
    """

    def __init__(self):
        # Connect signals to stop handling method
        signal.signal(signal.SIGINT, self.stop_server)
        signal.signal(signal.SIGTERM, self.stop_server)

        # Spyder kernels
        self._busy = None
        self._running = True
        self._kernels = {}
        self._current_properties = {}

        # Conda
        self._conda_manager = CondaManager()

        # Daemon server
        self._config = read_config()
        self._server_port = None

        # Zeroconf
        self._zeroconf = Zeroconf()
        self._service_port = find_free_port()
        self._service_info = None

    def get_properties(self):
        """
        Return properties to include in the zeroconf service. These properties
        include conda environments and local configuration values.

        Returns
        -------
        dic
            Properties dictionary.
        """
        envs = self._conda_manager.get_envs()
        valid_envs = set()
        valid_envs_has_kernels = set()
        for env_path in envs:
            env_name = os.path.basename(env_path)
            checks = []
            for pattern in self._config["exclude_environments"]:
                checks.append(not fnmatch.fnmatch(env_name, pattern))

            if all(checks):
                print(env_path)
                packages = self._conda_manager.list_packages(env_path)
                for item in packages:
                    check = item["dist_name"].startswith("spyder-kernels")
                    if check:
                        valid_envs_has_kernels.add(env_path)
                        break

                valid_envs.add(env_path)

        properties = {
            "server_port": self._server_port,
        }
        for i, env in enumerate(sorted(valid_envs)):
            if env in valid_envs_has_kernels:
                suffix = "yes"
            else:
                suffix = "no"

            properties[f"conda_env_{i}_{suffix}"] = env

        properties["guest_account"] = self._config["guest_account"]
        properties["name"] = self._config["name"]
        properties["max_kernels"] = self._config["max_kernels"]
        properties["guest_can_manage_environments"] = self._config[
            "guest_can_manage_environments"
        ]
        kernel_count = 0
        for env, kernel_data in self._kernels.items():
            kernel_count += len(kernel_data)

        properties["current_kernels"] = kernel_count

        return properties

    def get_service_info(self, properties=None):
        """
        Return the zeroconf service information.

        Returns
        -------
        zeroconf.ServiceInfo
            A zeroconf service object.
        """
        name = socket.gethostname() or platform.node()
        full_name = f"{name}.{SERVICE_TYPE}"
        if properties is None:
            self._current_properties = self.get_properties()
            properties = self._current_properties

        self._service_info = ServiceInfo(
            SERVICE_TYPE,
            full_name,
            port=self._service_port,
            properties=properties,  # key / value 255 len
            addresses=[socket.inet_aton(get_ip())],
        )
        return self._service_info

    def register_service(self):
        """
        Register zeroconf spyder remote service.
        """
        self._zeroconf.register_service(self.get_service_info())
        logger.info("Service registered!")
        print("Service registered!")

    def update_service(self):
        """
        Update service with updated information.
        """
        kernel_count = 0
        for _env, kernel_data in self._kernels.items():
            kernel_count += len(kernel_data)

        self._current_properties["current_kernels"] = kernel_count
        # self._zeroconf.update_service(self.get_service_info(self._current_properties))

    def start_kernel(self, prefix):
        """
        Start spyder-kernel located at environment prefix.

        Parameters
        ----------
        prefix: str
            Full path to conda environment prefix.
        """
        # FIXME: Use conda activation scripts
        python_path = f"{prefix}/bin/python"
        _, json_path = tempfile.mkstemp(suffix=".json")
        os.remove(json_path)
        cmd_args = [
            python_path,
            "-m",
            "spyder_kernels.console",
            f"--ip={get_ip()}",
            f"-f={json_path}",
        ]

        # To run as the guest user
        user_name = self._config["guest_account"]

        try:
            pw_record = pwd.getpwnam(user_name)
        except KeyError:
            print(f"User `{user_name}` not found!")
            return
        except Exception as err:
            print(f"Exception:\n {err}")
            return

        user_name = pw_record.pw_name
        user_home_dir = pw_record.pw_dir
        user_uid = pw_record.pw_uid
        user_gid = pw_record.pw_gid
        cwd = user_home_dir
        env = os.environ.copy()
        env["HOME"] = user_home_dir
        env["LOGNAME"] = user_name
        env["PWD"] = cwd
        env["USER"] = user_name
        try:
            kernel_proc = subprocess.Popen(
                cmd_args,
                preexec_fn=demote(user_uid, user_gid),
                cwd=cwd,
                env=env,
            )
        except Exception as error:
            print(error)

        if prefix not in self._kernels:
            self._kernels[prefix] = []

        time.sleep(1)
        while True:
            if os.path.isfile(json_path):
                with open(json_path, "r") as fh:
                    data = json.loads(fh.read())

                break
            time.sleep(1)

        self._kernels[prefix].append(
            {"process": kernel_proc, "kernel_data": data, "json_path": json_path}
        )
        print(f"The kernel process id: {kernel_proc.pid}")
        self.update_service()
        return data

    def stop_kernel(self, env=None):
        """
        Stop all kernels for given env if provided or all started kernels in no
        env is provided.
        """

    def start_server(self):
        """
        Start Spyder Remote server.
        """
        if not self._config["enable"]:
            print("Daemon not enabled. Check configuration!")
            return

        # self.start_kernel('/Users/goanpeca/miniconda3/envs/zeroconf')
        logger.info("Starting daemon!")
        logging.info("Starting daemon!")
        context = zmq.Context()
        socket = context.socket(zmq.REP)

        self._server_port = find_free_port()
        socket.bind(f"tcp://*:{self._server_port}")
        print(f"Bound to port {self._server_port}")
        self.register_service()

        while self._running:
            self._busy = True
            # Wait for next request from client
            message = socket.recv()

            try:
                reply = self.process_request(message)
            except Exception as err:
                reply = json.dumps({"error": str(err)})
                print(err)

            # reply = self.process_request(message)
            socket.send_string(reply)
            self._busy = False

    def process_request(self, message_byte_string):
        """
        Parameters
        ----------
        message_byte_string: bytes
            The request to process as a bytes string. When decoded it should
            provide a parseable JSON string.

        Examples
        --------
        >>> message_example_data = {
            "kernel": {
                "command": "start",
                "prefix": "conda-prefix",
            },
            "conda": {
                "command": "create",
                "prefix": "conda-env prefix",
                "name": "conda-env name",
                "packages": [],
            },
        }

        Returns
        -------
        str
            A JSON dumped string.
        """
        message = json.loads(message_byte_string.decode("utf-8"))
        print("Received request: %s" % message)

        reply = {"test": "testing"}
        if "kernel" in message:
            reply = self.handle_kernel_request(message)
        elif "conda" in message:
            reply = self.handle_conda_request(message)

        return json.dumps(reply)

    def handle_kernel_request(self, message):
        """
        Parameters
        ----------
        message: dict
            The message with kernel commands. {

        Example
        -------
        >>> {
            "kernel": {
                "command": "start",  # stop, close_all
                "prefix": "<prefix-to-conda-env>",
            }
        }

        Returns
        -------
        dict
            Response with a "json_data" key.
        """
        kernel_message = message["kernel"]
        command = kernel_message["command"]
        prefix = kernel_message.get("prefix", "")

        json_data = {}
        if command == "start" and prefix and os.path.isdir(prefix):
            json_data = self.start_kernel(prefix)
        elif command == "close_all":
            json_data = self.kill_running_kernels()

        return {"json_data": json_data}

    def handle_conda_request(self, message):
        """
        Handle conda requests to the server.

        Parameters
        ----------
        message: dict
            The message with kernel commands.

        Returns
        -------
        dict
            Response.
        """
        return {"status": "ok"}

    def kill_running_kernels(self):
        """
        Kill any kernels started by this server.

        Returns
        -------
        dict
            Response with a "status" key.
        """
        for env, kernels_data in self._kernels.items():
            for kernel_data in kernels_data:
                json_path = kernel_data["json_path"]
                os.remove(json_path)

                proc = kernel_data["process"]
                try:
                    print(f"Killing env: {env}")
                    logger.info(f"Killing env: {env}")
                    proc.terminate()
                    stdout, stderr = proc.communicate()
                except Exception as e:
                    logger.error(str(e))

        self._kernels = {}

        return {"status": "ok"}

    def stop_server(self, *args):
        """
        Handle sigterm signal to unregister services and kill any started
        kernels.
        """
        logger.info("Stopping Spyder Remote daemon!")
        self._running = False
        try:
            self._zeroconf.unregister_service(self._service_info)
        except Exception as e:
            logger.error(str(e))

        self.kill_running_kernels()
        sys.exit(0)


if __name__ == "__main__":
    server = SpyderRemoteServer()
    server.start_server()
