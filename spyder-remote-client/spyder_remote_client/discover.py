# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
import json
import os
import socket
import time

import psutil
from spyder_remote_client.constants import SERVICE_TYPE
from spyder_remote_client.utils import str2bool
from zeroconf import ServiceBrowser
from zeroconf import Zeroconf

os.environ["SPYDER_REMOTE_DEBUG"] = "1"


class SpyderRemoteListener:
    """
    Spyder remote Zeroconf listener.

    Notes
    -----
    https://github.com/jstasiak/python-zeroconf/blob/master/zeroconf/__init__.py#L1448
    """

    def __init__(self):
        self.hosts = {}
        self.hosts_properties = {}

    def _verbose(self):
        return bool(os.environ.get("SPYDER_REMOTE_DEBUG"))

    def add_service(self, zeroconf_instance, service_type, name):
        """
        Handle a zeroconf service addition.

        Parameters
        ----------
        zeroconf_instance: Zeroconf
            The zerconf instance.
        service_type: str
            The service type. Example: '_sdk._tcp.local.'
        name: str
            The name of the host exposing the service.
        """
        info = zeroconf_instance.get_service_info(service_type, name)
        new_info = {}
        for key, value in info.properties.items():
            new_info[key.decode()] = value.decode()

        self.hosts[name] = info
        self.hosts_properties[name] = new_info
        if self._verbose():
            print(f"adding service type '{service_type}' from '{name}'")
            print(info)

    def remove_service(self, zeroconf_instance, service_type, name):
        """
        Handle a zeroconf service removal.

        Parameters
        ----------
        zeroconf_instance: Zeroconf
            The zerconf instance.
        service_type: str
            The service type. Example: '_sdk._tcp.local.'
        name: str
            The name of the host exposing the service.
        """
        if name in self.hosts:
            del self.hosts[name]
            del self.hosts_properties[name]

        if self._verbose():
            print(f"removing service type '{service_type}' from '{name}'")

    def update_service(self, zeroconf_instance, service_type, name):
        """
        Handle a zeroconf service update.

        Parameters
        ----------
        zeroconf_instance: Zeroconf
            The zerconf instance.
        service_type: str
            The service type. Example: '_sdk._tcp.local.'
        name: str
            The name of the host exposing the service.
        """
        info = zeroconf_instance.get_service_info(service_type, name)
        self.hosts[name] = info

        if self._verbose():
            print(f"updating service type '{service_type}' from '{name}' to {info}")

    def get_hosts(self):
        """
        Return a dictionary with the host name as key, and the info associated
        with it as value.

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
            retval[host]["address"] = host_address
            retval[host]["port"] = self.hosts[host].port
            retval[host]["guest_account"] = properties["guest_account"]
            # retval[host]['guest_can_manage_environments'] = str2bool(properties['guest_can_manage_environments'])
            # retval[host]['status'] = properties['status']
            # retval[host]['local'] = host_address in my_addresses

        if self._verbose():
            print(retval)

        return retval


if __name__ == "__main__":
    zeroconf_instance = Zeroconf()
    listener = SpyderRemoteListener()
    browser = ServiceBrowser(zeroconf_instance, SERVICE_TYPE, listener)
    try:
        input("Press enter to exit...\n\n")
        time.sleep(2)
        print(listener.get_hosts())
    finally:
        zeroconf.close()
