# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

# Standard library imports
import ast
import os

# Third party imports
from setuptools import find_packages, setup

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='spyder_remote_client'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()

    lines = data.split('\n')
    for line in lines:
        if line.startswith('__version__'):
            version = ast.literal_eval(line.split('=')[-1].strip())
            break

    return version


setup(
    name="spyder-remote-client",
    version=get_version(),
    url="https://github.com/Semi-ATE/spyder-remote/tree/master/spyder-remote-client",
    description="",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        "netifaces",
        "psutil",
        # "spyder",
        "zeroconf",
    ],
    entry_points={
        'console_scripts': [
            'cmd = loghub.cli.main:main',
        ],
        "spyder.plugins": [
            "spyder_remote = spyder_remote_client.plugin:SpyderRemote"
        ]
    },
)
