# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote Container.
"""

from qtpy.QtCore import Signal
from spyder.api.translations import get_translation
from spyder.api.widgets.main_container import PluginMainContainer

from spyder_remote_client.spyder.widgets import RemoteConsoleDialog

# Localization
_ = get_translation("spyder_remote_client")


class SpyderRemoteContainer(PluginMainContainer):
    def __init__(self, name, plugin, parent=None):
        super().__init__(name, plugin, parent=parent)

        self._dialog = RemoteConsoleDialog(self)
        self._dialog.sig_connect_to_kernel.connect(self.sig_connect_to_kernel)
        self._dialog.setModal(True)

    # --- Signals
    # ------------------------------------------------------------------------
    sig_connect_to_kernel = Signal(object)
    """
    This signal is emitted with the json data to perform the connection to the
    remote spyder-kernel.

    Parameters
    ----------
    json_data: dict
        The kernel spec file with the information to perform the connection.
    """

    # --- PluginMainContainer API
    # ------------------------------------------------------------------------
    def setup(self):
        pass

    def on_option_update(self, options, value):
        pass

    def update_actions(self):
        pass

    # --- Public API
    # ------------------------------------------------------------------------
    def new_remote_console(self):
        """
        Connect to a remote console.
        """
        self._dialog.clear()
        self._dialog.setup()
        self._dialog.show()

    def close_all_kernels(self):
        """
        Close all kernels started on this session.
        """
        self._dialog.close_all_kernels()

    def close_services(self):
        """
        Close zeroconf services.
        """
        if self._dialog:
            self._dialog.close()

    @property
    def kernels(self):
        """Kernels started by Spyder remote client."""
        return self._dialog._kernels
