# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote Container.
"""

from qtpy.QtCore import Signal
from spyder.api.translations import get_translation
from spyder.api.widgets import PluginMainContainer

from spyder_remote_client.spyder.widgets import RemoteConsoleDialog

# Localization
_ = get_translation("spyder_remote_client")


class SpyderRemoteContainer(PluginMainContainer):
    DEFAULT_OPTIONS = {}

    def __init__(self, name, plugin, parent=None, options=DEFAULT_OPTIONS):
        super().__init__(name, plugin, parent=parent, options=options)

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
    def setup(self, options=DEFAULT_OPTIONS):
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
        self._dialog.setup()
        self._dialog.show()

    def close_all_kernels(self):
        """
        Close all kernels started on this session.
        """
        self._dialog.close_all_kernels()
