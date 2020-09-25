# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

# Standard library imports
import json
import os
import pwd
import subprocess
import sys



WIN = os.name == 'nt'


def run_process(cmd_list):
    """Run subprocess with cmd_list and return stdour, stderr, error."""
    stdout = ''
    stderr = ''
    error = False
    try:
        p = subprocess.Popen(
            cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()
    except OSError:
        error = True

    return stdout, stderr, error


def is_conda_available():
    """Check if conda is available in path."""
    return bool(get_conda_cmd_path())


def get_conda_cmd_path():
    """Check if conda is found on path."""
    cmds = []
    conda_path = None
    bin_folder = 'Scripts' if WIN else 'bin'
    conda_exe = 'conda-script.py' if WIN else 'conda'
    env_prefix = os.path.dirname(os.path.dirname(sys.prefix))

    cmds.append(os.path.join(env_prefix, bin_folder, conda_exe))
    cmds.append(os.path.join(sys.prefix, bin_folder, conda_exe))
    cmds.append('conda')

    for cmd in cmds:
        cmd_list = [cmd, '--version']
        stdout, stderr, error = run_process(cmd_list)
        if not error:
            if stdout.startswith('conda ') or stderr.startswith('conda '):
                conda_path = cmd
                break

    return conda_path


def get_conda_info():
    """Return conda info as a dictionary."""
    conda_cmd = get_conda_cmd_path()
    info = None
    if conda_cmd:
        cmd_list = [conda_cmd, 'info', '--json']
        out, err, error = run_process(cmd_list)
        try:
            info = json.loads(out)
        except Exception:
            pass

    return info


def get_username():
    """
    https://stackoverflow.com/a/2899055
    """
    return pwd.getpwuid(os.getuid())[0]
