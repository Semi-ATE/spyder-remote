# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file '/Users/goanpeca/Dropbox (Personal)/develop/tdk/spyder-remote/spyder-remote-client/spyder_remote_client/spyder/dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(448, 354)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(140, 25))
        self.label.setMaximumSize(QtCore.QSize(140, 25))
        self.label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spyderHosts = QtWidgets.QComboBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(130, 25))
        self.label_4.setMaximumSize(QtCore.QSize(130, 25))
        self.label_4.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(130, 25))
        self.label_5.setMaximumSize(QtCore.QSize(130, 25))
        self.label_5.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.password = QtWidgets.QLineEdit(self.credentials)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(130, 25))
        self.label_2.setMaximumSize(QtCore.QSize(130, 25))
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.condaEnvironments = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(
            self.condaEnvironments.sizePolicy().hasHeightForWidth()
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(130, 25))
        self.label_6.setMaximumSize(QtCore.QSize(130, 25))
        self.label_6.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
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
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
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
        self.spyderHosts.setItemText(
            0, _translate("Dialog", "Gonzalo Peña-Castellanos' Raspberry Pi")
        )
        self.spyderHosts.setItemText(1, _translate("Dialog", "local"))
        self.spyderHosts.setItemText(2, _translate("Dialog", "Carlos' Mac Book pro"))
        self.spyderHosts.setItemText(3, _translate("Dialog", "Ralf's Server"))
        self.spyderHosts.setItemText(4, _translate("Dialog", "Tom's MiniSCT"))
        self.credentials.setTitle(_translate("Dialog", "Credentials :"))
        self.label_4.setText(_translate("Dialog", "User :"))
        self.user.setItemText(0, _translate("Dialog", "goanpeca"))
        self.user.setItemText(1, _translate("Dialog", "nerohmot"))
        self.label_5.setText(_translate("Dialog", "Password :"))
        self.password.setPlaceholderText(_translate("Dialog", "from keyring"))
        self.keyring.setText(_translate("Dialog", "Store/Update Password in keyring"))
        self.groupBox.setTitle(_translate("Dialog", "Conda :"))
        self.label_2.setText(_translate("Dialog", "Environment :"))
        self.condaEnvironments.setToolTip(
            _translate("Dialog", "Select the remote conda environment to work in")
        )
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
