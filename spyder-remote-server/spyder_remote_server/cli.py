# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote command line interface.
"""

import os
import subprocess
import sys

import click
from daemoniker import send, SIGINT
from spyder_remote_server.api import get_cpu_count, install_daemon, uninstall_daemon
from spyder_remote_server.constants import AUTO, PID_FILE_PATH

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))
DAEMON_FILE = "daemon.py"
DAEMON_PATH = os.path.join(HERE, DAEMON_FILE)


@click.group(
    help=(
        "Spyder Remote Server provides Spyder IDE kernels for conda "
        "environments using zeroconf."
    )
)
def main():
    pass


@main.command(help=("Install the server daemon"))
@click.argument("guest", type=click.STRING)
@click.argument("cores", type=click.INT, default=AUTO)
def install(guest, cores):
    """
    --guest [guest_account] it will also add a guest account to the system
    (with the same password as the account) and add this info also to the
    `/etc/spyder-remote.conf` file.

    Cores: and it will set the maximum numbers of consoles this machine will provide.
    """
    # click.echo("Install the server daemon")
    new_cores = get_cpu_count(cores)
    if cores != new_cores:
        click.echo(f"Using '{new_cores}' cores!")

    try:
        install_daemon(guest, new_cores)
    except PermissionError as e:
        click.echo("You need to install the daemon with sudo!")


@main.command(help=("Uninstall the server daemon"))
def uninstall():
    # click.echo("Uninstall the server daemon")

    try:
        uninstall_daemon()
    except PermissionError as e:
        click.echo("You need to uninstall the daemon with sudo!")
    except FileNotFoundError as e:
        pass


@main.command(help=("Start the server daemon"))
def start():
    # click.echo("Uninstall the server daemon")
    try:
        subprocess.Popen([sys.executable, DAEMON_PATH])
    except Exception as e:
        print(e)
        click.echo("Daemon already started!")


@main.command(help=("Stop the server daemon"))
def stop():
    try:
        # Send a SIGINT to a process denoted by a PID file
        send(PID_FILE_PATH, SIGINT)
        click.echo("Daemon stopped!")
    except Exception as e:
        click.echo("Daemon not started!")
