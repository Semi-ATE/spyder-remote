# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:51:04 2020

@author: Tom Hören

    best would be maybe to follow PEP3143 ( https://www.python.org/dev/peps/pep-3143/ )
    for daemonizing, although that also follows Stevens...
    In any case the packages we might want to use are:
      - python-daemon
        - https://pagure.io/python-daemon/tree/master
        - https://pypi.org/project/python-daemon/
        - https://github.com/conda-forge/python-daemon-feedstock
        - https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
        ➜ only Linux & MacOS but has a feedstock although no aarch64 support
      - daemoniker
        - https://github.com/Muterra/py_daemoniker
        - https://pypi.org/project/daemoniker/
        - https://daemoniker.readthedocs.io/en/latest/
        ➜ Linux, MacOS and Windows, but no feedstock

    We need a solution that is installable (prefferable) via conda (conda-forge channel)
    and for sure needs to have `aarch64` support!

    For now we stick with Linux, and implement a well behaved daemon ourselves
    for the sake of the proof of concept.

    other references :
      - pid : https://serverfault.com/questions/417892/how-to-find-the-pid-file-for-a-given-process
      - configparser : https://docs.python.org/3/library/configparser.html
      - jinja2 : https://jinja.palletsprojects.com
"""

import os
import sys
import platform
import shutil
import psutil
import configparser
import zeroconf
import time
import atexit
import signal

import pprint

from configparser import NoOptionError

mode = "development"

if not sys.version_info[0] == 3:
    raise Exception("not running on python3 !")


class SKSD:
    """A generic daemon abstract base class for python3 under Linux"""

    verbose = True
    debug = True

    def __init__(self, config_dir=None):
        self.can_start = True

        # name
        self.name = self.__class__.__name__.lower()
        if self.verbose:
            print(f"daemon name = '{self.name}'")

        # os & id's
        self.OS = platform.system()
        if self.OS == "Linux":
            self.euid = os.geteuid()
            self.uid = os.getuid()
            if config_dir is None:
                self.config_dir = "/etc"
            else:
                self.config_dir = config_dir
            self.pid_dir = "/var/run"
        else:
            self.can_start = False
            if self.debug:
                print(f"can_start = {self.can_start} (debugging mode)")
                self.euid = "?"
                self.uid = "?"
                self.config_dir = os.path.dirname(__file__)
                self.pid_dir = os.path.dirname(__file__)
            else:
                raise Exception(f"Unknown OS : '{self.OS}'")
        if not os.path.exists(self.config_dir):
            raise Exception(f"Configuration directory '{self.config_dir}' does not exist")
        if not os.path.exists(self.pid_dir):
            raise Exception(f"PID directory '{self.pid_dir}' does not exist")
        if self.verbose:
            print(f"Operating System = '{self.OS}'")
            print(f"Configuration Directory = '{self.config_dir}'")
            print(f"PID Directory = '{self.pid_dir}'")
            print(f"euid = '{self.euid}'")
            print(f"uid = '{self.uid}'")

        # configuration
        self.config = configparser.ConfigParser()

        # configuration (boolean states)
        self.config.BOOLEAN_STATES = {
            "1": True,
            "on": True,
            "On": True,
            "ON": True,
            "true": True,
            "True": True,
            "TRUE": True,
            "yes": True,
            "YES": True,
            "Yes": True,
            "y": True,
            "Y": True,
            "sure": True,
            "Sure": True,
            "SURE": True,
            "yup" : True,
            "Yup" : True,
            "YUP" : True,
            #
            "0": False,
            "off": False,
            "Off": False,
            "OFF": False,
            "false": False,
            "False": False,
            "FALSE": False,
            "no": False,
            "No": False,
            "NO": False,
            "n": False,
            "N": False,
            "nope": False,
            "Nope": False,
            "NOPE": False}

        # configuration (define the default configuration)
        self.DEFAULT = {
            "enable": "False",
            "name": "",
            "guest_account": "",
            "guest_can_manage_environments": "True",
            "max_kernels": "AUTO",
            "exclude_environments" : "['base', '_*']"}
        self.config["DEFAULT"] = self.DEFAULT

        # configuration (generate if needed and read the configuration file)
        self.config_file = os.path.join(self.config_dir, f"{self.name}.conf")
        if self.verbose:
            print(f"Config file = '{self.config_file}'")
        if not os.path.exists(self.config_file):
            self.write_default_config_file()
        if self.verbose:
            print("Reading config file ... ", end="")
        self.config.read(self.config_file)
        if self.verbose:
            print("Done.")
            self.print_configuration()
            print("Post-processing configuration file ... ", end="")
        # configuration (post-processing)
        for key in self.config["DEFAULT"]:
            if key in ['enable', 'guest_can_manage_environments']:
                value = str(self.config["DEFAULT"].getboolean(key))
                self.config.set("DEFAULT", key, value)
            if "\n" in self.config['DEFAULT'][key]:
                value = self.config['DEFAULT'][key].replace('\n', '|')
                self.config.set("DEFAULT", key, value)
            if key == "max_kernels":
                value = self.config['DEFAULT'][key]
                cores = psutil.cpu_count()
                if value.upper().startswith('AUTO'):
                    value = str(cores - 1)
                if 'CORES' in value:
                    value = value.replace('CORES', str(cores))
                value = str(int(eval(value)))
                self.config.set("DEFAULT", key, value)
        for section in self.config.sections():
            for key in self.config["DEFAULT"]:
                if key in ['enable', 'guest_can_manage_environments']:
                    value = str(self.config["DEFAULT"].getboolean(key))
                    self.config.set("DEFAULT", key, value)
                if "\n" in self.config['DEFAULT'][key]:
                    value = self.config['DEFAULT'][key].replace('\n', '|')
                    self.config.set("DEFAULT", key, value)
                if key == "max_kernels":
                    value = self.config['DEFAULT'][key]
                    cores = psutil.cpu_count()
                    if value.upper().startswith('AUTO'):
                        value = str(cores - 1)
                    if 'CORES' in value:
                        value = value.replace('CORES', str(cores))
                    value = str(int(eval(value)))
                    self.config.set("DEFAULT", key, value)
        if self.verbose:
            print("Done.")
            self.print_configuration()
        if not self.config['DEFAULT'].getboolean('enable'):
            self.can_start = False
            if self.verbose:
                print("Config file prevents the daemon from starting.")

        # pid file
        self.pid_file = os.path.join(self.pid_dir, f"{self.name}.pid")
        if self.verbose:
            print(f"pid-file = '{self.pid_file}'")
        if os.path.exists(self.pid_file):
            pid, ctime = self.read_pid_file()
            if self.verbose:
                print(f"pid-file exists (pid={pid}, ctime={ctime})")
            if psutil.pid_exists(pid):
                if self.verbose:
                    print(f"process with pid={pid} is running")
                creation_time = int(psutil.Process(pid).create_time())
                if creation_time == ctime:
                    if self.verbose:
                        print(f"process with pid={pid} is the owner of the pid-file.")
                    self.can_start = False
                    if self.verbose:
                        print(f"preventing this process to daemonize.")
                else:
                    if self.verbose:
                        print(f"process with pid={pid} is not the owner of the pid-file.")
                        print("removing pid-file ... ", end="")
                    os.remove(self.pid_file)
                    if self.verbose:
                        print("Done.")
            else:
                if self.verbose:
                    print(f"process with pid={pid} is not running, delete pid file ... ", end="")
                os.remove(self.pid_file)
                if self.verbose:
                    print("Done.")

    def write_default_config_file(self, path):
        """Write the default configuration (setup is in pre_run) to the config file in `path`"""
        from jinja2 import Environment, FileSystemLoader

        file_loader = FileSystemLoader()
        env = Environment(loader=file_loader)

        template_file = os.path.join(os.path.dirname(__file__), f"{self.name}.jinja2")
        template = env.get_template(template_file)

        output = template.render(content=self.DEFAULT)
        if self.verbose:
            print(f"'{self.config_file}' doesn't exist, creating ... ", end="")
        print(output)
        if self.verbose:
            print("Done.")

    def print_configuration(self):
        print("  [DEFAULT]")
        for key in self.config["DEFAULT"]:
            print(f"    {key} = {self.config['DEFAULT'][key]}")

        for section in self.config.sections():
            print(f"  [{section}]")
            for key in self.config[section]:
                print(f"    {key} = {self.config[section][key]}")

    def read_pid_file(self):
        """This method reads the pid-file, and returns the tuple (pid, ctime)"""
        pid = -1
        ctime = -1
        with open(self.pid_file, 'r') as fd:
            lines = fd.readlines()
        for line in lines:
            if line.startswith('pid'):
                pid = int(line.split('=')[1].strip())
            if line.startswith('ctime'):
                ctime = int(line.split('=')[1].strip())
        return (pid, ctime)

    def write_pid_file(self, pid):
        """This method writes the pid-file with the contents:

            pid = 123456
            ctime = 654321

        Returns True on success, and False on failure.
        if the file already exists, False will be returned, and nothing is done.
        if the supplied pid has no associated process, False will be returned.
        """
        def do_write(file_name, pid, ctime):
            if os.path.exists(file_name):
                os.remove(file_name)
            try:
                with open(file_name, 'w') as fd:
                    fd.write(f"pid = {pid}\n")
                    fd.write(f"ctime = {ctime}\n")
            except Exception:
                if os.path.exists(file_name):
                    os.remove(file_name)
                return False
            else:
                return True

        if os.path.exists(self.pid_file):
            pid_from_file, ctime_from_file = self.read_pid_file()
            if psutil.pid_exists(pid_from_file):
                ctime = int(psutil.Process(pid_from_file).create_time())
                if ctime == ctime_from_file:
                    return False
                else:
                    return do_write(self.pid_file, pid, int(psutil.Process(pid).create_time()))
            else:
                return do_write(self.pid_file, pid, int(psutil.Process(pid).create_time()))
        else:
            return do_write(self.pid_file, pid, int(psutil.Process(pid).create_time()))

    def __del__(self):
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def start(self):
        """Start the daemon."""

        def daemonize():
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)  # exit first parent
            except OSError as err:
                sys.stderr.write(f"fork #1 failed: {err}")
                sys.exit(1)

            # decouple from parent environment
            os.chdir('/')
            os.setsid()
            os.umask(0)

            # do second fork
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)  # exit from second parent
            except OSError as err:
                sys.stderr.write(f"fork #2 failed: {err}")
                sys.exit(1)

            # redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = open(os.devnull, 'r')
            so = open(os.devnull, 'a+')
            se = open(os.devnull, 'a+')

            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            # make very sure that the destructor is called when we die
            atexit.register(self.__del__)

            # go!
            self.run()

        if self.can_start:
            if os.path.exists(self.pid_file):
                pid_from_file, ctime_from_file = self.read_pid_file()
                if psutil.pid_exists(pid_from_file):
                    ctime = psutil.Process(pid_from_file).create_time()
                    if ctime == ctime_from_file:
                        print(f"{self.name} already running, aborting new instanse start.")
                        sys.exit(1)
                    else:
                        daemonize()
                else:
                    daemonize()
            else:
                daemonize()
        else:
            if self.verbose:
                print(f"can not start.")

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pid_file
        pid_to_kill, _ = self.read_pid_file()

        if psutil.pid_exists(pid_to_kill):
            try:
                while True:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.1)
            except OSError as err:
                e = str(err.args)
                if e.find("No such process") > 0:
                    if os.path.exists(self.pid_file):
                        os.remove(self.pid_file)
                else:
                    print(str(err.args))
                    sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """This is the daemon main loop"""

        # write the pid file
        self.write_pid_file(os.getpid())

        # TODO: get a free port number !
        # publish
        # go in loop mode


if __name__ == "__main__":
    name = '.'.join(os.path.basename(__file__).split('.')[:-1])
    if mode.upper().startswith("DEV"):
        config_dir = os.path.dirname(__file__)
    else:
        config_dir = os.path.join(os.path.sep, "etc", name)

    sksd = SKSD(config_dir)
    sksd.start()
