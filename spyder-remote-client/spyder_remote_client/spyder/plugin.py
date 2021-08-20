# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote Plugin.
"""

import json
import os
import tempfile
import uuid

from qtpy.QtGui import QIcon

# from spyder.api.plugins import Plugins, SpyderDockablePlugin
# from spyder.api.plugin_registration.decorators import on_plugin_available
# from spyder.config.base import get_translation

from spyder.api.plugins import Plugins, SpyderPluginV2
from spyder.api.translations import get_translation
from spyder.api.plugin_registration.decorators import on_plugin_available
from spyder.plugins.mainmenu.api import ApplicationMenus, ConsolesMenuSections

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
    REQUIRES = [Plugins.MainMenu]
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

    def on_initialize(self):
        container = self.get_container()
        self.new_remote_client_action = self.create_action(
            SpyderRemoteActions.NewRemoteConsole,
            text=_("New remote Console"),
            triggered=self.new_remote_console,
            register_shortcut=True,
        )
        self.close_all_kernels_action = self.create_action(
            SpyderRemoteActions.CloseRemoteKernels,
            text=_("Close remote kernels"),
            triggered=self.close_all_kernels,
            register_shortcut=True,
        )
        container.sig_connect_to_kernel.connect(self.start_remote_kernel)
        container.sig_connect_to_kernel.connect(lambda x: self.update_actions())
        self.close_all_kernels_action.setEnabled(False)

    @on_plugin_available(plugin=Plugins.MainMenu)
    def on_MainMenu_available(self):
        self.get_plugin(Plugins.MainMenu).add_item_to_application_menu(self.new_remote_client_action, menu_id=ApplicationMenus.Consoles, section=ConsolesMenuSections.New)
        self.get_plugin(Plugins.MainMenu).add_item_to_application_menu(self.close_all_kernels_action, menu_id=ApplicationMenus.Consoles, section=ConsolesMenuSections.New)

    def on_close(self, cancellable=True):
        self.close_all_kernels()
        self.close_services()
        return True

    def update_actions(self):
        self.close_all_kernels_action.setEnabled(bool(self.get_container().kernels))

    # --- API
    # ------------------------------------------------------------------------
    def close_all_kernels(self):
        """
        Close all kernels started on this session.
        """
        self.get_container().close_all_kernels()
        self.update_actions()
        self.sig_status_message_requested.emit(
            _("Spyder Remote Server: Closing all Kernels..."),
            5000,
        )

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
        connection_file = os.path.join(
            tempfile.tempdir,
            str(uuid.uuid4()) + ".json",
        )
        with open(connection_file, "w") as fh:
            fh.write(json.dumps(json_data["json_data"]))

        self.main.ipyconsole._create_client_for_kernel(
            connection_file, None, None, None
        )

    def close_services(self):
        """
        Close zeroconf services.
        """
        self.get_container().close_services()
