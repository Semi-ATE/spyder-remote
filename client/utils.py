#!/usr/bin/env python3
# -*- coding': utf-8 -*-
"""
Created on Sat Jun 20 09:21:26 2020

@author': nerohmot
"""

import os
import time
import platform
if platform.system() != 'Windows':
    import fcntl # is this linux only ?
import struct
import socket
import netifaces
import json
import urllib3
import OpenSSL

#from OpenSSL import crypto, SSL

rIFF = {0x0001: 'UP',           # Interface is up.
        0x0002: 'BROADCAST',    # Broadcast address valid.
        0x0004: 'DEBUG',        # Turn on debugging.
        0x0008: 'LOOPBACK',     # Is a loopback net.
        0x0010: 'POINTOPOINT',  # Interface is point-to-point link.
        0x0020: 'NOTRAILERS',   # Avoid use of trailers.
        0x0040: 'RUNNING',      # Resources allocated.
        0x0080: 'NOARP',        # No address resolution protocol.
        0x0100: 'PROMISC',      # Receive all packets.
        0x0200: 'ALLMULTI',     # Receive all multicast packets.
        0x0400: 'MASTER',       # Master of a load balancer.
        0x0800: 'SLAVE',        # Slave of a load balancer.
        0x1000: 'MULTICAST',    # Supports multicast.
        0x2000: 'PORTSEL',      # Can set media type.
        0x4000: 'AUTOMEDIA',    # Auto media select active.
        0x8000: 'DYNAMIC'}      # Dialup device with changing addresses.


def ifstatus(ifname):
    """This function returns the status of 'ifname' as a set of human readable flags."""
    # TODO: make it work for both U*IX and Windows
    SIOCGIFFLAGS = 0x8913
    null256 = '\0' * 256
    retval = set()

    if ifname in netifaces.interfaces():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        result = fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, ifname + null256)
        flags, = struct.unpack('H', result[16:18])
        for flag in rIFF:
            if flag & flags == flag:
                retval.add(rIFF[flag])
    return retval


def is_local_ipv4(addr):
    """This function returns True if 'addr' is a local IP V4 address."""
    if addr in local_ipv4():
        return True
    return False


def is_local_ipv6(addr):
    """This function returns True if 'addr' is a local IP V6 address."""
    if addr in local_ipv6():
        return True
    return False


def is_local_ip(addr):
    """This function returns True if 'addr' is a local IP V4 or V6 address."""
    return is_local_ipv4(addr) or is_local_ipv6(addr)


def local_ipv4():
    """This function returns a list of all local IP V4 addresses."""
    retval = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        for address in addresses[netifaces.AF_INET]:
            retval.append(address['addr'])
    return retval


def local_ipv6():
    """This function returns a list of all local IPV6 addresses."""
    retval = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        for address in addresses[netifaces.AF_INET6]:
            retval.append(address['addr'])
    return retval


def local_ip():
    """This function returns a list of all IP addresses."""
    return local_ipv4() + local_ipv6()


def get_domain_name():
    """This function returns the domain name."""
    retval = socket.getfqdn().replace(socket.gethostname(), "")
    if retval.startswith('.'):
        retval = retval[1:]
    return retval



def str2bool(string):
    """This function converts a string to a boolean."""
    return string.lower() in ("yes", "y", "true", "t", "1")


class self_signed_certificate:
    """Self Signed Certificate, valid for 15 years.

    references:
        - https://stackoverflow.com/questions/27164354/create-a-self-signed-x509-certificate-in-python
        - https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
    """

    def __init__(self, email=None, sn=0):
        data = json.loads(urllib3.PoolManager().request('GET', 'http://ipinfo.io/json').data.decode("utf-8"))
        self.key = OpenSSL.crypto.PKey()
        self.key.generate_key(OpenSSL.crypto.TYPE_RSA, 4096)
        self.certificate = OpenSSL.crypto.X509()
        self.certificate.get_subject().C = data['country']
        self.certificate.get_subject().ST = data['region']
        self.certificate.get_subject().L = f"{data['postal']} {data['city']}"
        self.certificate.get_subject().O = data['org']
        self.certificate.get_subject().OU = f"{data['ip']}@{int(time.time())}"
        self.certificate.get_subject().CN = data['loc']
        if email is None:
            self.certificate.get_subject().emailAddress = "fu@bar"
        else:
            self.certificate.get_subject().emailAddress = email
        self.certificate.set_serial_number(sn)
        self.certificate.gmtime_adj_notBefore(0)
        self.certificate.gmtime_adj_notAfter(15 * 365 * 24 * 60 * 60)
        self.certificate.set_issuer(self.certificate.get_subject())
        self.certificate.set_pubkey(self.key)
        self.certificate.sign(self.key, 'sha512')

    def write(self, path=None):
        """This method will write the certificate and the private key to path."""
        if path is None:
            path = os.getcwd()
        path = os.path.abspath(path)

        if not os.path.exists(path):
            raise Exception(f"{path} does not exist")

        with open(os.path.join(path, "selfsigned.crt"), "wt") as f:
            f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, self.certificate).decode("utf-8"))

        with open(os.path.join(path, "private.key"), "wt") as f:
            f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, self.key).decode("utf-8"))

def is_self_signed_certificate(cert_path):
    """This function returns True if 'cert' is a self signed certificate."""







if __name__ == "__main__":
    # ssc = self_signed_certificate()
    # ssc.write()
    ips = local_ip() + ['1.2.3.4']
    for ip in ips:
        print(f"'{ip}' {('is not a local', 'is a local')[is_local_ip(ip)]} ip address")

    print(get_domain_name())
