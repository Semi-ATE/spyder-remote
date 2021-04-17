# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote Widgets.
"""

import json
import time

import zmq
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QDialog
from zeroconf import ServiceBrowser, Zeroconf

from spyder_remote_client.constants import SERVICE_TYPE
from spyder_remote_client.spyder.dialog import Ui_Dialog
from spyder_remote_client.spyder.discover import QSpyderRemoteListener


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

        self._listener.sig_service_added.connect(self.service_updated)
        self._listener.sig_service_removed.connect(self.service_updated)
        self._listener.sig_service_updated.connect(self.service_updated)

        # Start zeroconf service browser
        self._browser = ServiceBrowser(
            self._zeroconf_instance,
            SERVICE_TYPE,
            self._listener,
        )

    def service_updated(self, zeroconf, service_type, service_name):
        self.setup()

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
                server_port = properties["server_port"]
                address = properties["address"]
                context = zmq.Context()

                #  Socket to talk to server
                # print("Connecting to hello world server…")
                socket = context.socket(zmq.REQ)
                socket.connect(f"tcp://{address}:{server_port}")
                data = {"kernel": {"command": "close_all"}}
                message = json.dumps(data)
                print("Sending request %s …" % message)
                socket.send_string(message)

                #  Get the reply.
                message = socket.recv()
                data = json.loads(message.decode("utf-8"))
                print("Received reply %s" % (data))

            self._kernels = []

    def connect(self):
        """
        Connect to selected kernel.
        """
        self.feedback_label.setText("Requesting new remote kernel...")

        properties = self.host_combo.currentData()
        server_port = properties["server_port"]
        address = properties["address"]
        context = zmq.Context()

        #  Socket to talk to server
        socket = context.socket(zmq.REQ)
        full_address = f"tcp://{address}:{server_port}"
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(full_address)
        prefix = self.env_comvo.currentData()
        data = {"kernel": {"command": "start", "prefix": prefix}}
        send_message = json.dumps(data)
        received_message = None

        if socket.poll(timeout=1000, flags=zmq.POLLOUT) != 0:
            print("Sending request %s …" % send_message)
            socket.send_string(send_message, flags=zmq.NOBLOCK)
            if socket.poll(timeout=5000, flags=zmq.POLLIN) != 0:
                try:
                    received_message = socket.recv(flags=zmq.NOBLOCK)
                except Exception:
                    pass

        if received_message:
            print("RECEIVED", received_message)
            self.feedback_label.setText("Starting remote kernel...")
            data = json.loads(received_message.decode("utf-8"))

            error = data.get("error")
            if error:
                self.feedback_label.setText("Spyder remote server error")
                raise Exception(f"Spyder remote server error:\n\n{error}")
            else:
                self._kernels.append(prefix)
                print("Received reply %s" % (data))
                self.sig_connect_to_kernel.emit(data)
                socket.disconnect(full_address)
                socket.close(linger=0)
                context.term()
                self.accept()
        else:
            self.clear()
            self.feedback_label.setText(f"Spyder remote server not responding!")
            self.connect_button.setEnabled(False)
            socket.disconnect(full_address)
            socket.close(linger=0)
            context.term()

    def clear(self):
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
