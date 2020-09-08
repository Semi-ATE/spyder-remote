# Copyright (c) Tom Hören.
# Distributed under the terms of the MIT License.
from setuptools import find_packages, setup


setup(
    name="spyder-remote-server",
    version="0.1.0",
    url="https://github.com/Semi-ATE/spyder-remote/tree/master/spyder-remote-server",
    description="",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        "netifaces",
        "psutil",
        "zeroconf",
    ],
    entry_points={
        'console_scripts': [
            'cmd = loghub.cli.main:main',
        ]
    },
)
