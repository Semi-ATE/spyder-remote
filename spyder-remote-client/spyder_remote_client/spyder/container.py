# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

"""
Spyder Remote Container.
"""

# Standard library imports
from collections import OrderedDict

# Third party imports
from qtpy.QtCore import QSize, Qt, Signal, Slot
from qtpy.QtWidgets import QDialog, QMenu, QToolBar
from spyder.api.exceptions import SpyderAPIError
from spyder.api.translations import get_translation
from spyder.api.widgets import PluginMainContainer

# Local imports
from spyder_remote_client.spyder.widgets import RemoteConsoleDialog

# Localization
_ = get_translation('spyder')


# --- Constants
# ------------------------------------------------------------------------

class ToolBarMenus:
    ToolBarsMenu = "toolbars_menu"


class ToolBarsMenuSections:
    Main = "main_section"
    Secondary = "secondary_section"


class ToolBarActions:
    ShowToolBars = "show toolbars"


class SpyderRemoteContainer(PluginMainContainer):
    DEFAULT_OPTIONS = {
    }

    def __init__(self, name, plugin, parent=None, options=DEFAULT_OPTIONS):
        super().__init__(name, plugin, parent=parent, options=options)

        self._dialog = RemoteConsoleDialog(self)
        self._dialog.sig_connect_to_kernel.connect(self.sig_connect_to_kernel)
        self._dialog.setModal(True)

    # Signals
    sig_connect_to_kernel = Signal(object)

    # --- Private Methods
    # ------------------------------------------------------------------------

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
        self._dialog.setup()
        self._dialog.show()

    def close_all_kernels(self):
        self._dialog.close_all_kernels()
