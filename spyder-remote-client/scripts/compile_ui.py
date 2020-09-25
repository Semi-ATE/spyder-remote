# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

import subprocess

from spyder_remote_client.spyder import DIALOG_UI_PATH

# Constants
def main():
    output = DIALOG_UI_PATH.replace(".ui", ".py")
    args = ["pyuic5", DIALOG_UI_PATH, "-o", output]
    p = subprocess.Popen(args)
    print(" ".join(args))
    stdout, stderr = p.communicate()
    print(stdout, stderr)


# TODO:
# Replace this line
# from PyQt5 import QtCore, QtGui, QtWidgets
# With
# from qtpy import QtCore, QtGui, QtWidgets


if __name__ == "__main__":
    main()
