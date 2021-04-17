# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote Widgets.
"""

import json
import time

import zmq
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QDialog, QMessageBox
from zeroconf import ServiceBrowser, Zeroconf

from spyder_remote_client.constants import SERVICE_TYPE
from spyder_remote_client.spyder.dialog import Ui_Dialog
from spyder_remote_client.spyder.discover import QSpyderRemoteListener
from spyder_remote_client.exceptions import SpyderRemoteServerException


class RemoteConsoleDialog(QDialog):

    # Signals
    # ------------------------------------------------------------------------
    sig_connect_to_kernel = Signal(object)
    """
    This signal is emitted with the json data to perform the connection to the
    remote spyder-kernel.

    Parameters
    ----------
    json_spec: dict
        The kernel spec file with the information to perform the connection.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._dialog_ui = Ui_Dialog()
        self._dialog_ui.setupUi(self)
        self._zeroconf_instance = Zeroconf()
        self._listener = QSpyderRemoteListener()
        self._kernels = []

        # Widgets
        self.host_combo = self._dialog_ui.spyderHosts
        self.user_combo = self._dialog_ui.user
        self.env_comvo = self._dialog_ui.condaEnvironments
        self.req = self._dialog_ui.requirements
        self.req_label = self._dialog_ui.label_6
        self.keyring_check = self._dialog_ui.keyring
        self.password = self._dialog_ui.password
        self.cancel_button = self._dialog_ui.cancelButton
        self.connect_button = self._dialog_ui.connectButton
        self.load_req_button = self._dialog_ui.findRequirements
        self.feedback_label = self._dialog_ui.feedback

        self.feedback_label.setText("")
        self.setWindowTitle("Connect to remote kernel")

        # Signals
        self.cancel_button.clicked.connect(self.close)
        self.connect_button.clicked.connect(self.connect)
        self.host_combo.currentIndexChanged.connect(self.change_host)

        self._listener.sig_service_added.connect(self._on_service_update)
        self._listener.sig_service_removed.connect(self._on_service_update)
        self._listener.sig_service_updated.connect(self._on_service_update)

        # Start zeroconf service browser
        self._browser = ServiceBrowser(
            self._zeroconf_instance,
            SERVICE_TYPE,
            self._listener,
        )

    def _on_service_update(self, zeroconf, service_type, service_name):
        """
        Update dialog on Zeroconf updates.

        Parameters
        ----------
        zeroconf : zeroconf.Zeroconf
            Zeroconf instance.
        service_type : str
            Zeroconf service type.
        service_name : str
            Zeroconf name type.
        """
        if self.isVisible():
            self.clear()
            self.setup()

    def _send(self, address, server_port, data):
        """
        Send data via zmq to Spyder Remote Server with address and port.

        Parameters
        ----------
        address : zeroconf.Zeroconf
            Spyder remote server address.
        server_port : str
            Spyder remote server port.
        data : dict
            Data to send to server.
        """
        received_message = None
        received_data = {}

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        full_address = f"tcp://{address}:{server_port}"
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(full_address)

        if socket.poll(timeout=1000, flags=zmq.POLLOUT) != 0:
            send_message = json.dumps(data)
            print("Sending request %s …" % send_message)
            socket.send_string(send_message, flags=zmq.NOBLOCK)
            if socket.poll(timeout=5000, flags=zmq.POLLIN) != 0:
                try:
                    received_message = socket.recv(flags=zmq.NOBLOCK)
                except zmq.Again:
                    pass

        if received_message:
            print("Received message %s …" % received_message)
            received_data = json.loads(received_message.decode("utf-8"))

        socket.disconnect(full_address)
        socket.close(linger=0)
        context.term()

        return received_data

    # --- Qt overrides
    # ------------------------------------------------------------------------
    def close(self):
        """
        Override Qt method.

        Close the zeroconf service browser.
        """
        self._zeroconf_instance.close()
        return super().close()

    # --- Public API
    # ------------------------------------------------------------------------
    def close_all_kernels(self):
        """
        Close all kernels started on this session.
        """
        hosts = self._listener.get_hosts()
        if self._kernels:
            for _host, properties in hosts.items():
                address = properties["address"]
                server_port = properties["server_port"]
                data = {"kernel": {"command": "close_all"}}
                self._send(address, server_port, data)

            self._kernels = []

    def connect(self):
        """
        Connect to selected kernel.
        """
        self.feedback_label.setText("Requesting new remote kernel...")

        properties = self.host_combo.currentData()
        address = properties["address"]
        server_port = properties["server_port"]

        prefix = self.env_comvo.currentData()
        data = {"kernel": {"command": "start", "prefix": prefix}}
        received_data = self._send(address, server_port, data)

        if received_data:
            self.feedback_label.setText("Starting remote kernel...")
            error = data.get("error")
            if error:
                self.feedback_label.setText("Spyder remote server error")
                raise SpyderRemoteServerException(error)
            else:
                self._kernels.append(prefix)
                self.sig_connect_to_kernel.emit(received_data)

            self.accept()
        else:
            self.clear()
            self.feedback_label.setText(f"Spyder remote server not responding!")
            self.connect_button.setEnabled(False)

    def clear(self):
        """Clear comboboxes and information text."""
        self.host_combo.clear()
        self.user_combo.clear()
        self.env_comvo.clear()
        self.feedback_label.setText("")

    def setup(self):
        """
        Setup the comboboxes.
        """
        self.req.setVisible(False)
        self.req_label.setVisible(False)
        self.load_req_button.setVisible(False)
        self.keyring_check.setDisabled(True)
        self.password.setDisabled(True)

        hosts = self._listener.get_hosts()

        for _host, properties in hosts.items():
            self.host_combo.addItem(properties["name"], properties)

        self.connect_button.setEnabled(bool(hosts))

    def change_host(self):
        """
        Update user and environment when a different host has been selected.
        """
        self.env_comvo.clear()
        self.user_combo.clear()
        _current_text = self.host_combo.currentText()
        properties = self.host_combo.currentData()
        if properties is not None:
            self.user_combo.addItem(properties["guest_account"])
            for key, value in properties.items():
                if key.startswith("conda_env_") and key.endswith("_yes"):
                    env_name = value.split("/")[-1]
                    self.env_comvo.addItem(env_name, value)
