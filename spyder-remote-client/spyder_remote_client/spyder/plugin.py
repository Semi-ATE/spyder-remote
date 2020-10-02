# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote Plugin.
"""

import json
import tempfile

from qtpy.QtGui import QIcon
from spyder.api.plugins import Plugins, SpyderPluginV2
from spyder.api.translations import get_translation
from spyder_remote_client.spyder.container import SpyderRemoteContainer

# Localization
_ = get_translation("spyder_remote_client")


# --- Constants
# ----------------------------------------------------------------------------
class SpyderRemoteActions:
    NewRemoteConsole = "new_remote_console_action"
    CloseRemoteKernels = "close_remote_kernels"


# --- Plugin
# ----------------------------------------------------------------------------
class SpyderRemote(SpyderPluginV2):
    """
    Spyder Remote Plugin.
    """

    NAME = "spyder_remote"
    REQUIRES = []
    CONTAINER_CLASS = SpyderRemoteContainer
    CONF_SECTION = NAME

    # --- SpyderPluginV2 API
    # ------------------------------------------------------------------------
    def get_name(self):
        return _("Spyder Remote Client")

    def get_description(self):
        return _("Discover Spyder kernels via zeroconf.")

    def get_icon(self):
        return QIcon()

    def register(self):
        container = self.get_container()
        self.new_remote_client_action = self.create_action(
            SpyderRemoteActions.NewRemoteConsole,
            text=_("New remote Console"),
            triggered=self.new_remote_console,
            # context=Qt.ApplicationShortcut,
            # shortcut_context="_",
            register_shortcut=True,
        )
        self.close_all_kernels_action = self.create_action(
            SpyderRemoteActions.CloseRemoteKernels,
            text=_("Close remote kernels"),
            triggered=self.close_all_kernels,
            # context=Qt.ApplicationShortcut,
            # shortcut_context="_",
            register_shortcut=True,
        )
        main_consoles_menu = self.main.consoles_menu_actions
        main_consoles_menu.insert(0, self.new_remote_client_action)
        main_consoles_menu.insert(1, self.close_all_kernels_action)
        container.sig_connect_to_kernel.connect(self.start_remote_kernel)

        print("Finished registering Spyder-Remote!")

    def on_close(self, cancellable=True):
        self.close_all_kernels()
        return True

    # --- API
    # ------------------------------------------------------------------------
    def close_all_kernels(self):
        """
        Close all kernels started on this session.
        """
        self.get_container().close_all_kernels()

    def new_remote_console(self):
        """
        Connect to a remote console.
        """
        self.get_container().new_remote_console()

    def start_remote_kernel(self, json_data):
        """
        Parameters
        ----------
        json_data: dict
            The kernel spec file with the information to perform the
            connection.
        """
        _, connection_file = tempfile.mkstemp(suffix=".json")
        with open(connection_file, "w") as fh:
            fh.write(json.dumps(json_data["json_data"]))

        self.main.ipyconsole._create_client_for_kernel(
            connection_file, None, None, None
        )
