# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
import os

SERVICE_TYPE = "_sdk._tcp.local."
DISCOVER_SERVICE_TYPE = "_spyder_remote_discover._tcp.local."
KERNEL_SERVICE_TYPE = "_spyder_remote_kernel._tcp.local."

# Number of cores
AUTO = 0

HERE = os.path.abspath(os.path.dirname(__file__))
PID_FILE = "daemon.pid"
PID_FILE_PATH = os.path.join(HERE, PID_FILE)
