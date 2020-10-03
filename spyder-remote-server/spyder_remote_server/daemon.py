# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
# https://github.com/torfsen/python-systemd-tutorial
# https://daemoniker.readthedocs.io/en/latest/
import os
import tempfile
import time

from daemoniker import Daemonizer
from daemoniker import SignalHandler1
from spyder_remote_server.constants import PID_FILE_PATH
from spyder_remote_server.server import SpyderRemoteServer


def do_things_here():
    print("Before daemonization")


def parent_only_code():
    print("Parent yei!")


def code_continues_here():
    print("code continues here!")
    server = SpyderRemoteServer()
    try:
        server.start_server()
    except Exception as e:
        server.stop()
    finally:
        server.stop()


with Daemonizer() as (is_setup, daemonizer):
    if is_setup:
        # This code is run before daemonization.
        # TODO: This has to run as `root`
        do_things_here()

    # We need to explicitly pass resources to the daemon; other variables
    # may not be correct
    is_parent = daemonizer(PID_FILE_PATH)

    if is_parent:
        # Run code in the parent after daemonization
        parent_only_code()


# We are now daemonized, and the parent just exited.


# Create a signal handler that uses the daemoniker default handlers for
# ``SIGINT``, ``SIGTERM``, and ``SIGABRT``
sighandler = SignalHandler1(PID_FILE_PATH)
sighandler.start()

# Or, define your own handlers, even after starting signal handling
def handle_sigint(signum):
    print("SIGINT received.")


sighandler.sigint = handle_sigint

print("code continues here!")
server = SpyderRemoteServer()
try:
    server.start_server()
except Exception as e:
    server.stop()
finally:
    server.stop()
