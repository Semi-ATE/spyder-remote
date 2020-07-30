#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:47:05 2020

@author: nerohmot
"""

import os
import socket
import time

from contextlib import closing
from zeroconf import IPVersion, ServiceInfo, Zeroconf

mode = "Development"
config_file_name = "skd.conf"

if mode != "Development":
    config_file_location = os.path.join(os.path.basedir(__file__), config_file_name)
else:
    config_file_location = "/etc/..."  # TODO: depends on OS ...


def find_free_port():
    """find free port"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def get_configuration():
    """This function creates a zeroconf.ServiceInfo object from the configuration file."""
    service = "_sksd._tcp.local."
    retval = ServiceInfo(
        service,
        f"{name}.{service}"

        )
    return retval


# def register_spyder_kernel(zeroconf, info):
#     zeroconf.register_service(info)


# def unregister_spyder_kernel(info):
#     zeroconf = Zeroconf(ip_version=IPVersion.All)
#     zeroconf.unregister_service(info)


# def update_spyder_kernel(info):
#     zeroconf.update_service(info)


def create_info(name, addresses, port, desc=[], service="_sksd._tcp.local."):
    return ServiceInfo(
        service,
        f"{name}.{service}",
        addresses=[socket.inet_aton("127.0.0.1")],  # ?!?
        properties=desc,
        server=socket.gethostname(),
    )


if __name__ == '__main__':
    zeroconf = Zeroconf(ip_version=IPVersion.All)

    info = ServiceInfo("Tom's MiniSCT",)


    info = create_info("Tom's MiniSCT", addresses, port)

    print("registering ...")
    zeroconf.register_service(info)
    time.sleep(60)
    print("unregistering ...")
    zeroconf.unregister_service(info)
