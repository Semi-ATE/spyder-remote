#!/usr/bin/env python3

"""
Example of announcing a service (in this case, a fake HTTP server)


https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/NetServices/Articles/domainnames.html

Bonjour Names for Existing Service Types
Bonjour services are named according to the existing Internet standard for IP services (described in RFC 2782). Bonjour service names combine service types and transport protocols to form a registration type. The registration type is used to register a service and create DNS resource records for it. To distinguish registration types from domain names in DNS resource records, registration types use underscore prefixes to separate the components that make up a registration type. The format is

_ServiceType._TransportProtocolName.

The service type is the official IANA-registered name for the service, for example, ftp, http or printer. The transport protocol name is tcp or udp, depending on the transport protocol the service uses. An FTP service running over TCP would have a registration type of _ftp._tcp. and would register a DNS PTR record named _ftp._tcp.local. with its hosts’ Multicast DNS responder.

_ftp._tcp.local.


Spyder Kernel Server Daemon  TCP  Local (zeroconf)
_sksd._tcp.local.
"""

from contextlib import closing
import argparse
import fnmatch
import logging
import os
import platform
import signal
import socket
import time
import json
import subprocess
import tempfile
import sys
from time import sleep

import zmq

from zeroconf import IPVersion, ServiceInfo, Zeroconf

from spyder_remote_server.constants import SERVICE_TYPE
from spyder_remote_server.conda_api import CondaManager
from spyder_remote_server.config import read_config, get_log_path

logging.basicConfig(
    filename=get_log_path(),
    filemode='a',
    format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



def find_free_port():
    """find free port"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class SpyderRemoteServer:
    def __init__(self):
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
        TODO:
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
                    check = item['dist_name'].startswith('spyder-kernels')
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
        properties["guest_can_manage_environments"] = self._config["guest_can_manage_environments"]
        kernel_count = 0
        for env, kernel_data in self._kernels.items():
            kernel_count += len(kernel_data)

        properties["current_kernels"] = kernel_count

        return properties

    def get_service_info(self, properties=None):
        """
        TODO:
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
            properties=properties,
            # addresses=[socket.inet_aton("127.0.0.1")],  # important!
            addresses=[socket.inet_aton(get_ip())],  # important!
        )
        return self._service_info

    def register_service(self):
        """
        TODO:
        """
        self._zeroconf.register_service(self.get_service_info())
        logger.info('Service registered!')
        print("Service registered!")

    def update_service(self):
        """
        TODO:
        """
        kernel_count = 0
        for env, kernel_data in self._kernels.items():
            kernel_count += len(kernel_data)

        self._current_properties["current_kernels"] = kernel_count
        # self._zeroconf.update_service(self.get_service_info(self._current_properties))

    def start_kernel(self, env):
        """
        TODO:
        """
        # FIXME: Use conda activation scripts
        python_path = f"{env}/bin/python"
        _, json_path = tempfile.mkstemp(suffix=".json")
        os.remove(json_path)
        cmd_args = [python_path, "-m", "spyder_kernels.console",  f"--ip={get_ip()}", f"-f={json_path}"]
        kernel_proc = subprocess.Popen(cmd_args)
        if env not in self._kernels:
            self._kernels[env] = []

        time.sleep(1)
        while True:
            if os.path.isfile(json_path):
                with open(json_path, "r") as fh:
                    data = json.loads(fh.read())

                break
            time.sleep(1)

        self._kernels[env].append({"process": kernel_proc, "kernel_data": data, "json_path": json_path})
        print(kernel_proc.pid)
        self.update_service()
        return data

    def stop_kernel(self, env=None):
        """
        Stop all kernels for given env if provided or all started kernels in no
        env is provided.
        """

    def start_server(self):
        """
        TODO:
        """
        if not self._config["enable"]:
            print("Daemon not enabled. Check configuration!")
            return

        logger.info('Starting daemon!')
        logging.info('Starting daemon!')
        context = zmq.Context()
        socket = context.socket(zmq.REP)

        self._server_port = find_free_port()
        socket.bind(f"tcp://*:{self._server_port}")
        print(f"Bound to port {self._server_port}")
        # self.start_kernel('/Users/goanpeca/miniconda3/envs/pip37')
        self.register_service()

        while self._running:
            #  Wait for next request from client
            self._busy = True
            message = socket.recv()
            reply = self.process_request(message)
            socket.send_string(reply)
            self._busy = False

    def process_request(self, message):
        """
        TODO:
        """
        message = json.loads(message.decode("utf-8"))
        print("Received request: %s" % message)
        # self.start_kernel('/Users/goanpeca/miniconda3/envs/pip37')

        message_example_data = {
            "kernel": {
                "command": "start",
                "prefix": "conda-prefix",
            },
            "conda": {
                "command": "create",
                "prefix": "conda-env prefix",
                "name": "conda-env name",
                "packages": [],
            }
        }

        reply = {"test": "testing"}
        if "kernel" in message:
            reply = self.handle_kernel_request(message)
        elif "conda" in message:
            reply = self.handle_conda_request(message)

        return json.dumps(reply)

    def handle_kernel_request(self, message):
        kernel_message = message["kernel"]
        command = kernel_message["command"]
        prefix = kernel_message.get("prefix", "")
        # Check if the prefix exists!
        json_data = {}
        if command == "start" and prefix and os.path.isdir(prefix):
            json_data = self.start_kernel(prefix)

        if command == "close_all":
            json_data = self.kill_running_kernels()

        return {"json_data": json_data}

    def handle_conda_request(self, message):
        return {"test": "conda"}

    def kill_running_kernels(self):
        # Killing any running kernels
        for env, kernels_data in self._kernels.items():
            for kernel_data in kernels_data:
                json_path = kernel_data["json_path"]
                os.remove(json_path)

                proc = kernel_data["process"]
                try:
                    print(f"Killing env: {env}")
                    proc.terminate()
                    stdout, stderr = proc.communicate()
                except Exception as e:
                    logger.error(str(e))

        self._kernels = {}
        return {"status": "ok"}

    def stop_server(self, *args):
        print("Stopping server!", args)
        logger.info('Stopping daemon!')
        self._running = False

        try:
            self._zeroconf.unregister_service(self._service_info)
        except Exception as e:
            logger.error(str(e))

        self.kill_running_kernels()
        sys.exit(0)


if __name__ == '__main__':
    server = SpyderRemoteServer()
    server.start_server()
