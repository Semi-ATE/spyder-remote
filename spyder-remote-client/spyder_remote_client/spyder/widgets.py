# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

import json

# Third party imports
import zmq
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QDialog
from zeroconf import Zeroconf, ServiceBrowser

# Local imports
from spyder_remote_client.constants import SERVICE_TYPE
from spyder_remote_client.spyder.dialog import Ui_Dialog
from spyder_remote_client.spyder.discover import QSpyderRemoteListener


class RemoteConsoleDialog(QDialog):

    sig_connect_to_kernel = Signal(object)

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

        # Signals
        self._listener.sig_service_added.connect(self.service_added)
        self.cancel_button.clicked.connect(self.close)
        self.connect_button.clicked.connect(self.connect)
        self.host_combo.currentIndexChanged.connect(self.change_host)
        # self._listener.sig_service_removed.connect()
        # self._listener.sig_service_updated.connect()

        self._browser = ServiceBrowser(
            self._zeroconf_instance,
            SERVICE_TYPE,
            self._listener,
        )

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
        """
        hosts = self._listener.get_hosts()
        if self._kernels:
            for host, properties in hosts.items():
                server_port = properties["server_port"]
                address = properties["address"]
                context = zmq.Context()

                #  Socket to talk to server
                # print("Connecting to hello world server…")
                socket = context.socket(zmq.REQ)
                socket.connect(f"tcp://{address}:{server_port}")
                data = {'kernel': {"command": 'close_all'}}
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
        """
        properties = self.host_combo.currentData()
        server_port = properties["server_port"]
        address = properties["address"]
        context = zmq.Context()

        #  Socket to talk to server
        # print("Connecting to hello world server…")
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{address}:{server_port}")
        prefix = self.env_comvo.currentData()
        data = {'kernel': {"command": 'start', "prefix": prefix}}
        message = json.dumps(data)
        print("Sending request %s …" % message)
        socket.send_string(message)

        #  Get the reply.
        message = socket.recv()
        data = json.loads(message.decode("utf-8"))
        self._kernels.append(prefix)
        self.sig_connect_to_kernel.emit(data)
        print("Received reply %s" % (data))
        self.accept()

    def service_added(self, zeroconf_instance, service_type, name):
        info = self._listener.hosts[name]

        # import zmq
        # import json

        # context = zmq.Context()

        # # Socket to talk to server
        # print("Connecting to hello world server…")
        # socket = context.socket(zmq.REQ)
        # socket.connect("tcp://localhost:56311")

        # data = {'kernel': {"command": 'start', "prefix": '/Users/goanpeca/miniconda3/envs/pip37'}}
        # message = json.dumps(data)
        # print("Sending request %s …" % message)
        # socket.send_string(message)

        # #  Get the reply.
        # message = socket.recv()
        # print("Received reply %s" % (message))

    def setup(self):
        self.host_combo.clear()
        self.user_combo.clear()
        self.env_comvo.clear()

        self.req.setVisible(False)
        self.req_label.setVisible(False)
        self.load_req_button.setVisible(False)
        self.keyring_check.setDisabled(True)
        self.password.setDisabled(True)

        hosts = self._listener.get_hosts()
        for host, properties in hosts.items():
            self.host_combo.addItem(properties["name"], properties)

    def change_host(self):
        self.env_comvo.clear()
        current_text = self.host_combo.currentText()
        properties = self.host_combo.currentData()
        if properties is not None:
            self.user_combo.addItem(properties["guest_account"])
            for key, value in properties.items():
                if key.startswith("conda_env_") and key.endswith("_yes"):
                    env_name = value.split("/")[-1]
                    self.env_comvo.addItem(env_name, value)

    def change_user(self):
        pass

    def change_environment(self):
        pass

"""
        Dialog.setObjectName("Dialog")
        Dialog.resize(448, 354)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(140, 25))
        self.label.setMaximumSize(QtCore.QSize(140, 25))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spyderHosts = QtWidgets.QComboBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.spyderHosts.sizePolicy().hasHeightForWidth())
        self.spyderHosts.setSizePolicy(sizePolicy)
        self.spyderHosts.setMinimumSize(QtCore.QSize(180, 25))
        self.spyderHosts.setObjectName("spyderHosts")
        self.spyderHosts.addItem("")
        self.spyderHosts.addItem("")
        self.spyderHosts.addItem("")
        self.spyderHosts.addItem("")
        self.spyderHosts.addItem("")
        self.horizontalLayout.addWidget(self.spyderHosts)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.credentials = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.credentials.sizePolicy().hasHeightForWidth())
        self.credentials.setSizePolicy(sizePolicy)
        self.credentials.setObjectName("credentials")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.credentials)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.credentials)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(130, 25))
        self.label_4.setMaximumSize(QtCore.QSize(130, 25))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.user = QtWidgets.QComboBox(self.credentials)
        self.user.setObjectName("user")
        self.user.addItem("")
        self.user.addItem("")
        self.horizontalLayout_3.addWidget(self.user)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.credentials)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(130, 25))
        self.label_5.setMaximumSize(QtCore.QSize(130, 25))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.password = QtWidgets.QLineEdit(self.credentials)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password.sizePolicy().hasHeightForWidth())
        self.password.setSizePolicy(sizePolicy)
        self.password.setMinimumSize(QtCore.QSize(160, 25))
        self.password.setMaximumSize(QtCore.QSize(16777215, 25))
        self.password.setClearButtonEnabled(True)
        self.password.setObjectName("password")
        self.horizontalLayout_4.addWidget(self.password)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.keyring = QtWidgets.QCheckBox(self.credentials)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyring.sizePolicy().hasHeightForWidth())
        self.keyring.setSizePolicy(sizePolicy)
        self.keyring.setMinimumSize(QtCore.QSize(0, 25))
        self.keyring.setMaximumSize(QtCore.QSize(16777215, 25))
        self.keyring.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.keyring.setChecked(True)
        self.keyring.setObjectName("keyring")
        self.verticalLayout.addWidget(self.keyring)
        self.verticalLayout_3.addWidget(self.credentials)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(130, 25))
        self.label_2.setMaximumSize(QtCore.QSize(130, 25))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.condaEnvironments = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.condaEnvironments.sizePolicy().hasHeightForWidth())
        self.condaEnvironments.setSizePolicy(sizePolicy)
        self.condaEnvironments.setMinimumSize(QtCore.QSize(180, 25))
        self.condaEnvironments.setObjectName("condaEnvironments")
        self.condaEnvironments.addItem("")
        self.condaEnvironments.addItem("")
        self.condaEnvironments.addItem("")
        self.condaEnvironments.addItem("")
        self.condaEnvironments.addItem("")
        self.condaEnvironments.addItem("")
        self.horizontalLayout_2.addWidget(self.condaEnvironments)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(25, 25))
        self.label_3.setMaximumSize(QtCore.QSize(25, 25))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(130, 25))
        self.label_6.setMaximumSize(QtCore.QSize(130, 25))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.requirements = QtWidgets.QComboBox(self.groupBox)
        self.requirements.setObjectName("requirements")
        self.requirements.addItem("")
        self.horizontalLayout_6.addWidget(self.requirements)
        self.findRequirements = QtWidgets.QToolButton(self.groupBox)
        self.findRequirements.setMinimumSize(QtCore.QSize(25, 25))
        self.findRequirements.setMaximumSize(QtCore.QSize(25, 25))
        self.findRequirements.setObjectName("findRequirements")
        self.horizontalLayout_6.addWidget(self.findRequirements)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.feedback = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.feedback.sizePolicy().hasHeightForWidth())
        self.feedback.setSizePolicy(sizePolicy)
        self.feedback.setMinimumSize(QtCore.QSize(0, 25))
        self.feedback.setMaximumSize(QtCore.QSize(16777215, 25))
        self.feedback.setAlignment(QtCore.Qt.AlignCenter)
        self.feedback.setObjectName("feedback")
        self.verticalLayout_3.addWidget(self.feedback)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_5.addWidget(self.cancelButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.connectButton = QtWidgets.QPushButton(Dialog)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout_5.addWidget(self.connectButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Remote Spyder Host :"))
        self.spyderHosts.setItemText(0, _translate("Dialog", "Gonzalo Peña-Castellanos\' Raspberry Pi"))
        self.spyderHosts.setItemText(1, _translate("Dialog", "local"))
        self.spyderHosts.setItemText(2, _translate("Dialog", "Carlos\' Mac Book pro"))
        self.spyderHosts.setItemText(3, _translate("Dialog", "Ralf\'s Server"))
        self.spyderHosts.setItemText(4, _translate("Dialog", "Tom\'s MiniSCT"))
        self.credentials.setTitle(_translate("Dialog", "Credentials :"))
        self.label_4.setText(_translate("Dialog", "User :"))
        self.user.setItemText(0, _translate("Dialog", "goanpeca"))
        self.user.setItemText(1, _translate("Dialog", "nerohmot"))
        self.label_5.setText(_translate("Dialog", "Password :"))
        self.password.setPlaceholderText(_translate("Dialog", "from keyring"))
        self.keyring.setText(_translate("Dialog", "Store/Update Password in keyring"))
        self.groupBox.setTitle(_translate("Dialog", "Conda :"))
        self.label_2.setText(_translate("Dialog", "Environment :"))
        self.condaEnvironments.setToolTip(_translate("Dialog", "Select the remote conda environment to work in"))
        self.condaEnvironments.setItemText(0, _translate("Dialog", "sandbox"))
        self.condaEnvironments.setItemText(1, _translate("Dialog", "base"))
        self.condaEnvironments.setItemText(2, _translate("Dialog", "anaconda3"))
        self.condaEnvironments.setItemText(3, _translate("Dialog", "_spyder_"))
        self.condaEnvironments.setItemText(4, _translate("Dialog", "MiniSCT"))
        self.condaEnvironments.setItemText(5, _translate("Dialog", "RPI"))
        self.label_6.setText(_translate("Dialog", "Requirements :"))
        self.requirements.setItemText(0, _translate("Dialog", "N/A"))
        self.findRequirements.setText(_translate("Dialog", "..."))
        self.feedback.setText(_translate("Dialog", "feedback line"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.connectButton.setText(_translate("Dialog", "Connect"))
"""
