# Copyright (c) Tom Hören.
# Distributed under the terms of the MIT License.
from setuptools import find_packages, setup


setup(
    name="spyder-remote-client",
    version="0.1.0",
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
