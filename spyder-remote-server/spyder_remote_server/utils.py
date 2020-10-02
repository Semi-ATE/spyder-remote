# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder remote server utilities.
"""

import json
import os
import pwd
import socket
import subprocess
import sys
from contextlib import closing

# Constants
WIN = os.name == "nt"


def demote(user_uid, user_gid):
    """
    Callback to use with subprocess `preexec_fn` to change the user running
    the process.

    Parameters
    ----------
    user_uid: int
        TODO:
    user_gid: int
        TODO:
    """

    def result():
        report_ids("starting demotion")
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids("finished demotion")

    return result


def report_ids(msg):
    print("uid, gid = %d, %d; %s" % (os.getuid(), os.getgid(), msg))


def run_process(cmd_list):
    """
    Run subprocess with cmd_list and return stdour, stderr, error.

    Returns
    -------
    tuple
        Tuple of stdout, stderr and any exception found.
    """
    stdout = ""
    stderr = ""
    error = False
    try:
        p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()
    except OSError:
        error = True

    return stdout, stderr, error


def is_conda_available():
    """
    Check if conda is available in path.

    Returns
    -------
    bool
        Wheter conda is available in the system.
    """
    return bool(get_conda_cmd_path())


def get_conda_cmd_path():
    """
    Check if conda is found on path.

    Returns
    -------
    str
        Path to conda executable.
    """
    cmds = []
    conda_path = None
    bin_folder = "Scripts" if WIN else "bin"
    conda_exe = "conda-script.py" if WIN else "conda"
    env_prefix = os.path.dirname(os.path.dirname(sys.prefix))

    cmds.append(os.path.join(env_prefix, bin_folder, conda_exe))
    cmds.append(os.path.join(sys.prefix, bin_folder, conda_exe))
    cmds.append("conda")

    for cmd in cmds:
        cmd_list = [cmd, "--version"]
        stdout, stderr, error = run_process(cmd_list)
        if not error:
            if stdout.startswith("conda ") or stderr.startswith("conda "):
                conda_path = cmd
                break

    return conda_path


def get_conda_info():
    """
    Return conda info as a dictionary.

    Returns
    -------
    dict
        Conda information.
    """
    conda_cmd = get_conda_cmd_path()
    info = None
    if conda_cmd:
        cmd_list = [conda_cmd, "info", "--json"]
        out, err, error = run_process(cmd_list)
        try:
            info = json.loads(out)
        except Exception:
            pass

    return info


def get_username():
    """
    Get the current username.

    https://stackoverflow.com/a/2899055
    """
    return pwd.getpwuid(os.getuid())[0]


def get_ip():
    """
    Get the public IP interface of the current machine.

    Returns
    -------
    str
        IP of current machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()

    return IP


def find_free_port():
    """
    Find free port.

    Returns
    -------
    int
        Free port found.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
