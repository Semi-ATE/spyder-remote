# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:51:04 2020

@author: Tom Hören

    best would be maybe to follow PEP3143 ( https://www.python.org/dev/peps/pep-3143/ )
    for daemonizing, although that also follows Stevens... in any case python-daemon
    is the package we then want to use ( https://pagure.io/python-daemon/tree/master )
    but the package to be installed via the conda-forge channel has no aarch64 support
    ( https://github.com/conda-forge/python-daemon-feedstock ) another option would
    be to use https://daemoniker.readthedocs.io/en/latest/ but I don't know that
    package (yet), that's why I implement a well behaved daemon based on stevens myself 😇

    references :
        https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
        https://serverfault.com/questions/417892/how-to-find-the-pid-file-for-a-given-process
"""

import sys
import os
import time
import atexit
import signal
import platform

from configparser import NoOptionError

from abc import ABC, abstractmethod


if not sys.version_info[0] == 3:
    raise Exception("not running on python3 !")


class daemon_ABC(ABC):
    """A generic daemon abstract base class for python3 under Linux"""

    verbose = True
    enabled = True

    def __init__(self, config_dir=None):

        # name
        self.name = self.__class__.__name__.lower()
        if self.verbose:
            print(f"daemon name = '{self.name}'")

        # os & id's
        self.OS = platform.system()
        if self.OS == "Windows":
            self.euid = "?"
            self.uid = "?"
        elif self.OS in ["Linux", "Darwin"]:
            self.euid = os.geteuid()
            self.uid = os.getuid()
        else:
            raise Exception("Unknown OS : '{self.OS}'")
        if self.verbose:
            print(f"Operating System = '{self.OS}'")
            print(f"euid = '{self.euid}'")
            print(f"uid = '{self.uid}'")

        # configuration
        if config_dir is None:  # set automatically based on self.OS
            if self.OS == "Windows":
                self.config_dir = "?"
            elif self.OS == "Linux":
                self.config_dir = "/etc"
            elif self.OS == "Darwin":
                self.config_dir = "/etc"
        else:
            self.config_dir = config_dir
        self.config_file = os.path.join(self.config_dir, f"{self.name}.conf")
        if self.verbose:
            print(f"Config dir = '{self.config_dir}'")
            print(f"Config file = '{os.path.basename(self.config_file)}'")
        if not os.path.exists(self.config_dir):
            raise Exception(f"'{config_dir}' does not exist (or is not accessable)!")
        if not os.path.exists(self.config_file):
            if self.verbose:
                print("writing config file ... ", end="")
            self.write_default_config_file(self.config_file)
            if self.verbose:
                print("Done")









        if self.verbose:
            print(f"Configuration file = '{self.config_dir}'")






        self.pid_file = os.path.join(config_dir, f"{self.name}.pid")
        if self.verbose:
            print(f"pid-file = '{self.pid_file}'")
        # TODO: if the pid file exists, open it, look what process did write it, and
        # look if the process is running, if so, report and die, if not so, remove
        # the pid file and go on.
        if os.path.exists(self.pid_file):
            if self.verbose:
                printf(f"pid-file already exists, looking for process ...  ", end="")
            try:
                os.remove(self.pid_file)
            except Exception as e:
                if self.verbose:
                    print("Failed.")
                raise Exception(f"pid-file '{self.pid_file}' already exitst and can't be removed! ({e})")
            if self.verbose:
                print("Done.")

    @abstractmethod
    def write_default_config_file(self, path):
        pass

    def __del__(self):
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def daemonize(self):
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

        # write the pid file
        pid = str(os.getpid())
        with open(self.pid_file, 'w+') as f:
            f.write(pid + '\n')

        # make very sure that the destructor is called when we die
        atexit.register(self.__del__)

    def start(self):
        """Start the daemon."""

        # Check for a pid_file to see if the daemon already runs
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pid_file {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pid_file))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pid_file
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pid_file {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pid_file))
            return  # not an error in a restart

        # Try killing the daemon process
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

    def pre_run(self):
        """Deamon 'pre_run' business logic comes here."""
        pass

    @abstractmethod
    def run(self):
        """Deamon 'run' business logic comes here, (should be an endless loop)."""
        pass

    def post_run(self):
        """Deamon 'post_run' (and pre-exit) business logic comes here."""
        pass
