#!/usr/bin/env python3
# -*- coding': utf-8 -*-
"""
Created on Sat Jun 20 09:21:26 2020

@author': nerohmot
"""

import os
import sys
import time
import platform
import struct
import socket
import netifaces
import json
import urllib3
import OpenSSL
import subprocess
import tqdm

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

macOS_releases = {
    '10.0' : 'Cheetah',
    '10.1': 'Puma',
    '10.2': 'Jaguar',
    '10.3': 'Panther',
    '10.4': 'Tiger',
    '10.5': 'Leopard',
    '10.6': 'Snow Leopard',
    '10.7': 'Lion',
    '10.8': 'Mountain Lion',
    '10.9': 'Mavericks',
    '10.10': 'Yosemite',
    '10.11': 'El Capitan',
    '10.12': 'Sierra',
    '10.13': 'High Sierra',
    '10.14': 'Mojave',
    '10.15': 'Catalina',
    '11.0': 'Big Sur'}

class systemInfo:

    def __init__(self):
        self.is_linux = False
        self.is_macos = False
        self.is_windows = False

        self.machine = platform.machine()
        self.processor = platform.processor()
        if sys.maxsize > 2**32:
            self.bits = 64
        else:
            self.bits = 32
        self.endian = sys.byteorder
        system = platform.system().lower()
        if system == 'linux':
            self.is_linux = True
            self.os = 'Linux'
            need_more_info = True

            # 1. check /etc/os-release
            if need_more_info and os.path.isfile('/etc/os-release'):
                with open('/etc/os-release') as fd:
                    os_release = fd.read()
                for line in os_release.split(os.linesep):
                    if line.startswith('NAME='):
                        self.os += ' ' + line.split('=')[1].replace('"', '').replace('Linux', '').strip()
                    if line.startswith('VERSION='):
                        self.os += ' ' + line.split('=')[1].replace('"', '').strip()
                self.kernel = shell('uname -r')[1][0].strip()
                need_more_info = False

            # 2. check /etc/lsb-release (Linux Standard Base)
            # if need_more_info and os.path.isfile('/etc/lsb-release'):
            #     with open('/etc/lsb-release') as fd:
            #         lsb_release = fd.read()
            #     for line in lsb_release.split(os.linesep):
            #         if line.startswith('DISTRIB_DESCRIPTION='):
            #             self.os += ' ' + line.split('=')[1].replace('"', '').replace('Linux', '').strip()
            #     self.kernel = self._exec('uname -r')[1][0].strip()
            #     need_more_info = False

            # 3. check with hostnamectl
            # hostnamectl = self._which('hostnamectl')
            # if need_more_info and hostnamectl != '':
            #     exit_status, output = self._exec('hostnamectl')
            #     for line in output:
            #         if line.startswith('Operating System:'):
            #             self.os += ' ' + line.split(':')[1].strip()
            #         if line.startswith('Kernel:'):
            #             self.kernel = line.split(':')[1].strip()
            #     need_more_info = False


            #TODO: 'which evince' --> distutils.spawn.find_executable('evince')

            # 4. check /etc/redhat-release
            # 5. check /etc/system-release
            # 6. check /etc/system-release-cpe
            # 7. check /etc/issue


        elif system == 'darwin':
            self.is_macos = True
            mac_ver = platform.mac_ver()[0]
            mac_base_ver = '.'.join(mac_ver.split('.')[:2])
            if mac_base_ver in macOS_releases:
                mac_name = macOS_releases[mac_base_ver]
            else:
                mac_name = ''
            self.os = f'macOS {mac_name} ({mac_ver})'
            self.kernel = self._exec('uname -r')[1][0].strip()
        elif system == 'windows':
            self.is_windows = True
            self.os = f'Windows {platform.release()}'
            self.kernel = platform.version()

        self.host = socket.gethostname()
        self.fqdn = socket.getfqdn()
        self.domain = self.fqdn.replace(self.host, "")
        if self.domain.startswith('.'):
            self.domain = self.domain[1:]

    def __str__(self):
        return os.linesep.join([
            f"Operating System : {self.os}",
            f"          Kernel : {self.kernel}",
            f"       Processor : {self.processor} ({self.bits} bit {self.endian} endian)",
            f"            fqdn : {self.fqdn}"
            ])

    def _which(self, cmd):
        """This method returns whatever 'which cmd' is returning."""
        exit_code, out, err = shell(f"which {cmd}")
        if exit_code == 0:
            return out[0]
        else:
            return ''






class pythonInfo:
    """Python information."""

    def __init__(self):
        self.version = platform.python_version()
        self.executable = sys.executable
        self.implementation = platform.python_implementation()

    def __str__(self):
        return f"{self.implementation} {self.version}"

class condaInfo:
    """conda information."""
    def __init__(self):
        with open('conda_version_stdout.txt', 'w+') as fout:
            with open('conda_version_stderr.txt', 'w+') as ferr:
                conda_version_exit_status = subprocess.call(['conda', '--version'], stdout=fout, stderr=ferr)
                fout.seek(0)
                conda_version_stdout = fout.read()

        with open('conda_envs_stdout.txt','w+') as fout:
            with open('conda_envs_stderr.txt','w+') as ferr:
                conda_envs_exit_status = subprocess.call(["conda",'env', 'list'], stdout=fout, stderr=ferr)
                fout.seek(0)
                conda_envs_stdout = fout.read()

        self.available_envs = []
        self.active_env = ''
        if conda_version_exit_status == 0:  # conda is installed
            self.version = conda_version_stdout.strip().split()[1]
            if conda_envs_exit_status == 0:  # should always be as conda is installed
                if 'CONDA_DEFAULT_ENV' in os.environ:  # conda is active
                    self.active_env = os.path.basename(os.environ['CONDA_DEFAULT_ENV'])
                for environment in conda_envs_stdout.split(os.linesep):
                    if environment.startswith('#'):
                        continue
                    if environment == '':
                        continue
                    env = environment.split()[0]
                    self.available_envs.append(env)
                    if env == self.active_env:
                        self.active_env_prefix = environment.split()[2]
        if self.active_env == '':
            self.active = False
        else:
            self.active = True

    def __str__(self):
        return self.active_env

class ipInfo:

    def __init__(self):
        self.local_ipv4 = []
        self.local_ipv6 = []
        # fetch all local IPv4 addresses of the local interfaces
        for interface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(interface)
            for address in addresses[netifaces.AF_INET]:
                self.local_ipv4_addresses.append(address['addr'])
        # fetch all local IPv6 addresses of the local interfaces
        for interface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(interface)
            for address in addresses[netifaces.AF_INET6]:
                self.local_ipv6.append(address['addr'])
        self.local_ip = self.local_ipv4 + self.local_ipv6

    def is_local_ipv4(self, addr):
        """This method returns True if 'addr' is a local IP V4 address."""
        if addr in self.local_ipv4:
            return True
        return False

    def is_local_ipv6(self, addr):
        """This method returns True if 'addr' is a local IP V6 address."""
        if addr in self.local_ipv6:
            return True
        return False

    def is_local(self, addr):
        """This method return True if 'addr' is a local IP address."""
        if addr in self.local_ip:
            return True
        return False




def shell(cmd):
    """This function executes the 'cmd' in a subprocess.

    'cmd' must be a string.
    it returns exit_code, stdout, stderr as a tuple.
    both stdout and stderr are lists of lines
    both the stdout and stderr are stripped of white lines
    all lines are stripped of leading and lagging spaces.
    """
    stdout_retval = []
    stderr_retval = []
    exit_status = 255
    stdout_file = "stdout.txt"
    stderr_file = "stderr.txt"
    if isinstance(cmd, str):
        with open(stdout_file, 'w+') as fout:
            with open(stderr_file, 'w+') as ferr:
                exit_status = subprocess.call(cmd.split(), stdout=fout, stderr=ferr)
                fout.seek(0)
                stdout = fout.read().split(os.linesep)
                ferr.seek(0)
                stderr = ferr.read().split(os.linesep)
        os.remove(stdout_file)
        os.remove(stderr_file)
        for line in stdout:
            if line != '':
                stdout_retval.append(line.strip())
        for line in stderr:
            if line != '':
                stderr_retval.append(line.strip())
    return (exit_status, stdout_retval, stderr_retval)

def conda_status():
    python = pythonInfo()
    conda = condaInfo()
    if conda.active:
        return f"conda: {conda} ({python})"
    else:
        return "conda: inactive"

def ifstatus(ifname):
    """This function returns the status of 'ifname' as a set of human readable flags."""
    system = platform.system().lower()
    if system == 'linux':
        status, stdout, stdin = shell('ip link show')
        print(stdout)
        # ip link show
    elif system == 'darwin':
        pass # how to get the same thing from there?!?
    elif system == 'windows':
        import fcntl

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
    else:
        raise Exception(f"{platform.system()} operating system not supported.")






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
    import netifaces

    # for ifname in netifaces.interfaces():
    #     print(ifname)
    status, stdin, stdout = ifstatus('')
    for line in stdout(''):
        print(line)