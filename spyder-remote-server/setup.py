# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

"""
Spyder remote server setup.
"""

import ast
import os

from setuptools import find_packages
from setuptools import setup

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


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, "README.md"), "r") as f:
        data = f.read()
    return data


setup(
    name="spyder-remote-server",
    version=get_version(),
    url="https://github.com/Semi-ATE/spyder-remote/tree/master/spyder-remote-server",
    description="Spyder remote server to connect to Spyder kernels via zeroconf.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        # "netifaces",
        # "psutil",
        "click",
        "daemoniker",
        "jinja2",
        "zeroconf",
    ],
    entry_points={
        "console_scripts": [
            "spyder-remote-server = spyder_remote_server.cli:main",
        ]
    },
)
