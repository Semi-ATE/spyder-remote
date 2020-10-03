# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
# Standard library imports
import ast
import os

from setuptools import find_packages
from setuptools import setup

# Third party imports

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module="spyder_remote_server"):
    """Get version."""
    with open(os.path.join(HERE, module, "__init__.py"), "r") as f:
        data = f.read()

    lines = data.split("\n")
    for line in lines:
        if line.startswith("__version__"):
            version = ast.literal_eval(line.split("=")[-1].strip())
            break

    return version


setup(
    name="spyder-remote-server",
    version=get_version(),
    url="https://github.com/Semi-ATE/spyder-remote/tree/master/spyder-remote-server",
    description="",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        # "netifaces",
        # "psutil",
        "click",
        "jinja2",
        "zeroconf",
    ],
    entry_points={
        "console_scripts": [
            "spyder-remote-server = spyder_remote_server.cli:main",
        ]
    },
)
