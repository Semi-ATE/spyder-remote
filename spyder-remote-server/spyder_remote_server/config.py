# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Load and parse spyder-remote configuration.
"""

import ast
import configparser
import multiprocessing
import os
import platform
import socket
import sys

from jinja2 import Environment, PackageLoader, select_autoescape
from spyder_remote_server.constants import AUTO
from spyder_remote_server.templates import CONFIG_TEMPLATE

# Constants
INIFILE = "spyder-remote-server.ini"
DEFAULT_CONFIG = {
    ##############################################################################
    # The `enable` keyword will determine if the Spyder Kernels Daemon will start
    #
    # Notes:
    #  * if `enable` is not supplied, it is presumed turned off!
    #  * if `enable` can not be interpreted, it is presumed turned off!
    #
    "enable": False,
    ##############################################################################
    # The `name` is the 'pretty print' (host)name that will be published.
    # spaces, apostrops are allowed, it is a (UTF-8) string!
    # if `service_name` is not provided here, the system's hostname (not so pretty)
    # will be pasted in.
    #
    # Notes:
    #  * if no service `name` is provided, the service will not start!
    #
    "name": socket.gethostname() or platform.node(),
    ##############################################################################
    # The `guest_account` keyword determines as what guest `user` the sksd
    # will spin up the Spyder Kernels.
    #
    # If there is no `guest_account`, this means that the user needs to provide
    # valid credentials for this host system.
    #
    # Notes:
    #  * if the guest account needs a password, the format is "user:password"
    #  * if the guest account needs an empty string password, the format is "user:"
    #  * if the guest account doesn't need a password, the format is "user"
    #
    "guest_account": "sct",
    ##############################################################################
    # The `guest_can_manage_environments` keyword determines if a `guest`
    # is allowed to create/modify (guest) environments.
    #
    # Notes:
    #  * if no guest_account is provided, this option is disregarded.
    #  * a `user` (guest or not) can in any case not create/modify environments
    #    outside the scope of the user !
    #
    "guest_can_manage_environments": False,
    ##############################################################################
    # The `max_kernels` keyword determines the maximum number of spyder-kernels
    # `skd` can spinn up. This is a (positive) integer value. If the value can't
    # be interpreted, the fallback is '0'. '0' means automatic calculation, it
    # takes the number of CPU cores, deducts 1 and that is set. There is in
    # principle no upper limit ...
    #
    # Notes:
    #  * `skd` will publish the value for `max_kernels` as well as the number of
    #    kernels already spinned up.
    #  * AUTO means # CPU cores - 1
    #  * anything starting with 'auto' (regardless capitalization) is considered 'AUTO'
    #  * CORES = the number of CPU cores
    #  * simple calculations are possible the result will be casted to integer.
    #    eg: (CORES/2)-1 ➜ (8/2)-1 ➜ 3 for a 8 core machine.
    #
    # Default value = AUTO
    #
    "max_kernels": AUTO,
    ##############################################################################
    # The `exclude_environments` keyword determines what environments will **NOT**
    # be published. (regardless if they exist or not)
    #
    # Notes:
    #  * It **must** be a list
    #  * One can use a wildcard '*' in the list.
    #  * application environments (starting with '_') can also be excluded here.
    #  * If nothing is provided, the default value is presumed.
    #
    # Default value = ["base", "_*"]
    #
    "exclude_environments": ["base", "_*"],
}


def config_path():
    """
    Return the path of the system configuration file.

    Returns
    -------
    str:
        Path to configuration file.
    """
    if sys.platform.startswith("linux"):
        path = "/etc"
    else:
        path = os.path.expanduser("~/.spyder-remote-server")

    if not os.path.isdir(path):
        os.makedirs(path)

    return os.path.join(path, INIFILE)


def create_config(guest, cores):
    """
    Create a confguration file in the configuration folder.

    Parameters
    ----------
    guest: str
        Account to use as guest account.
    cores: int
        Maximum number of spyder-kernels allowed.
    """
    config = DEFAULT_CONFIG.copy()
    config["guest_account"] = guest
    config["max_kernels"] = cores
    config["enable"] = True

    env = Environment(loader=PackageLoader("spyder_remote_server", "templates"))
    template = env.get_template(CONFIG_TEMPLATE)
    data = template.render(config=config)

    with open(config_path(), "w") as fh:
        fh.write(data)


def remove_config():
    """
    Remove configuration file from configuration path.
    """
    try:
        os.remove(config_path())
    except Exception as e:
        print(e)


def read_config():
    """
    Read Spyder Remote configuration.

    If no configuration is found, the default configuration is returned.

    Returns
    -------
    dict
        Configuration dictionary.
    """
    fpath = config_path()
    config_parser = configparser.ConfigParser()
    if os.path.isfile(fpath):
        config_parser.read(fpath)
        config = {}
        for key, default_value in DEFAULT_CONFIG.items():
            value = config_parser["DEFAULT"][key]
            if isinstance(default_value, (list, float, bool, int)):
                value = ast.literal_eval(value)

            config[key] = value
    else:
        config = DEFAULT_CONFIG.copy()

    return config


def get_log_path():
    """
    Get the logging folder path.

    Returns
    -------
    str
        Path to logging folder.
    """
    path = os.path.expanduser("~/.spyder-remote")
    if not os.path.isdir(path):
        os.makedirs(path)

    return os.path.join(path, "spyder-remote-server.log")
