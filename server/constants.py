# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 14:01:47 2020

@author: hoeren
"""

import os

zeroconf_type = "_sksd._tcp.local."
project_root = os.path.dirname(os.path.abspath(__file__))

config_name = "sksd"
config_file = f"{config_name}.conf"
config_template = os.path.join(project_root, f"{config_name}.jinja2")