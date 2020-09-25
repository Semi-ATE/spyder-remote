#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 23:27:34 2020

@author: tom
"""

import time
import json
import os
import psutil
import socket

from zeroconf import ServiceBrowser, Zeroconf

from spyder_remote_client.constants import SERVICE_TYPE

os.environ["SPYDER_REMOTE_DEBUG"] = "1"


def str2bool(string):
    """This function converts a string to a boolean."""
    return string.lower() in ("yes", "y", "true", "t", "1")


class SpyderListener:
    """
    Spyder remote Zeroconf listener.

    Notes
    -----
    https://github.com/jstasiak/python-zeroconf/blob/master/zeroconf/__init__.py#L1448
    """

    verbose = True

    def __init__(self):
        self.hosts = {}
        self.hosts_properties = {}

    def _verbose(self):
        return bool(os.environ.get("SPYDER_REMOTE_DEBUG"))

    def add_service(self, zeroconf_instance, service_type, name):
        info = zeroconf_instance.get_service_info(service_type, name)
        new_info = {}
        for key, value in info.properties.items():
            new_info[key.decode()] = value.decode()

        self.hosts[name] = info
        self.hosts_properties[name] = new_info
        if self._verbose():
            print(f"adding service type '{service_type}' from '{name}'")
            print(info)

    def remove_service(self, zeroconf, service_type, name):
        if name in self.hosts:
            del self.hosts[name]
            del self.hosts_properties[name]

        if self._verbose():
            print(f"removing service type '{service_type}' from '{name}'")

    def update_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        self.hosts[name] = info
        if self._verbose():
            print(f"updating service type '{service_type}' from '{name}' to {info}")

    def get_hosts(self):
        """
        Return a dictionary with the host name as key, and the info
        associated with it as value.

        It is **not** simply a copy of self.hosts, we need to replace the
        local host with 'localhost' (and the interface).
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
            properties = self.hosts_properties[host].copy()
            retval[host] = properties
            retval[host]['address'] = host_address
            retval[host]['port'] = self.hosts[host].port
            retval[host]['guest_account'] = properties['guest_account']
            # retval[host]['guest_can_manage_environments'] = str2bool(properties['guest_can_manage_environments'])

            # retval[host]['status'] = properties['status']
            # retval[host]['local'] = host_address in my_addresses

        print(retval)
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
    zeroconf = Zeroconf()
    listener = SpyderListener()
    browser = ServiceBrowser(zeroconf, SERVICE_TYPE, listener)
    try:
        input("Press enter to exit...\n\n")
        time.sleep(2)
        print(listener.get_hosts())
    finally:
        zeroconf.close()

    # try:
    #     while True:
    #         key = input(">>>")
    #         if key == '':
    #             break
    #         elif key in ['h', 'help']:
    #             print("help⏎ = this help")
    #             print("list⏎ = list spyder-hostsd's")
    #             print("⏎ = exit (note: it can take a while)")
    #         elif key in ['l', 'list']:
    #             detected_hosts = spyder_listener.get_hosts()
    #             for host in detected_hosts:
    #                 pp_host(host, detected_hosts[host])
    # finally:
    #     zeroconf.close()
