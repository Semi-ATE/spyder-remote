# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 14:01:47 2020

@author: hoeren
"""

import os

zeroconf_type = "_spyder_remote._tcp.local."
project_root = os.path.dirname(os.path.abspath(__file__))

config_file = "spyder-remote.conf"
config_template = os.path.join(project_root, "server", config_file)