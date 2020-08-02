#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 23:27:34 2020

@author: tom
"""
import psutil
import socket

from spyder_remote.utils import str2bool
from spyder_remote.constants import zeroconf_type

class SpyderListener:
    """This is a listener implemented as according to
    https://github.com/jstasiak/python-zeroconf/blob/master/zeroconf/__init__.py#L1448
    """

    verbose = True

    def __init__(self):
        self.hosts = {}

    def remove_service(self, zeroconf, service_type, name):
        if service_type == zeroconf_type:
            del self.hosts[name]
            if self.verbose:
                print(f"removing service type '{service_type}' from '{name}'")

    def add_service(self, zeroconf, service_type, name):
        if service_type == zeroconf_type:
            info = zeroconf.get_service_info(type, name)
            self.hosts[name] = info
            if self.verbose:
                print(f"adding service type '{service_type}' from '{name}'")

    def update_service(self, zeroconf, service_type, name):
        if service_type == zeroconf_type:
            info = zeroconf.get_service_info(service_type, name)
            self.hosts[name] = info
            if self.verbose:
                print(f"updating service type '{service_type}' from '{name}' to {info}")

    def get_hosts(self):
        """Return a dictionary with the host name as key, and the info associated with it as value.

        It is **not** simply a copy of self.hosts, we need to replace the local host with 'localhost' (and the interface)
        """
        my_addresses = {}
        my_interfaces = psutil.net_if_addrs()
        for interface in my_interfaces:
            for nic in my_interfaces[interface]:
                if nic.family in [socket.AF_INET, socket.AF_INET6]:
                    my_addresses[nic.address] = interface

        retval = {}
        for host in self.hosts:
            if len(self.hosts[host].addresses) != 1:
                raise Exception(f"Yup, not yet implemented ... {self.hosts[host]}")
            host_address = socket.inet_ntoa(self.hosts[host].addresses[0])
            host_label = f"{host}"
            if host_address in my_addresses:
                host_label += " (local)"
            retval[host_label] = {}
            retval[host_label]['address'] = host_address
            retval[host_label]['port'] = self.hosts[host].port
            retval[host_label]['guest_account'] = self.hosts[host].properties[b'guest_account'].decode("utf-8")
            retval[host_label]['guest_can_manage_environments'] = str2bool(self.hosts[host].properties[b'guest_can_manage_environments'].decode("utf-8"))
            retval[host_label]['free_slots'] = int(self.hosts[host].properties[b'free_slots'].decode("utf-8"))
            retval[host_label]['status'] = self.hosts[host].properties[b'status'].decode("utf-8")
        return retval

def pp_host(host, info):
    print(host)
    print(f"    address = {info['address']}")
    print(f"    port = {info['port']}")
    print(f"    guest_account = {info['guest_account']}")
    print(f"    guest_can_manage_environments = {info['guest_can_manage_environments']}")
    print(f"    free_slots = {info['free_slots']}")
    print(f"    status = {info['status']}\n")

if __name__ == '__main__':
    from zeroconf import Zeroconf

    spyderListener = SpyderListener()
    zeroconf = Zeroconf()
    zeroconf.add_service_listener(zeroconf_type, spyderListener)

    try:
        while True:
            key = input(">>>")
            if key == '':
                break
            elif key in ['h', 'help']:
                print("help⏎ = this help")
                print("list⏎ = list spyder-hostsd's")
                print("⏎ = exit (note: it can take a while)")
            elif key in ['l', 'list']:
                detected_hosts = spyderListener.get_hosts()
                for host in detected_hosts:
                    pp_host(host, detected_hosts[host])
    finally:
        zeroconf.close()
