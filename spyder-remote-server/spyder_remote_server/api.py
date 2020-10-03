# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
import multiprocessing

from spyder_remote_server.config import create_config
from spyder_remote_server.config import remove_config


def register_service():
    """
    TODO:
    """


def get_cpu_count(cores=None):
    """
    TODO:
    """
    cpu_count = multiprocessing.cpu_count()
    cores = cores or cpu_count

    if cores <= cpu_count:
        cpu_count = cores
    elif cores == 0:
        cpu_count = cpu_count - 1
    else:
        # cores > cpu_count, using system cpu_count
        pass

    return cpu_count


def install_daemon(guest, cores):
    """
    TODO:
    """
    create_config(guest, cores)
    register_service()


def uninstall_daemon():
    """
    TODO:
    """
    remove_config()
