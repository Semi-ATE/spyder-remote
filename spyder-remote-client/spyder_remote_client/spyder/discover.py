# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

from qtpy.QtCore import Signal, QObject

from spyder_remote_client.discover import SpyderListener


class QSpyderRemoteListener(QObject, SpyderListener):
    """
    Connects the SpyderRemoteListener to Qt Signals.
    """

    sig_service_added = Signal(object, str, str)
    """
    TODO:

    Parameters
    ----------
    zeroconf: ServiceInfo
        TODO:
    service_type: str
        TODO:
    name: str
        TODO:
    """

    sig_service_removed = Signal(object, str, str)
    """
    TODO:

    Parameters
    ----------
    zeroconf: ServiceInfo
        TODO:
    service_type: str
        TODO:
    name: str
        TODO:
    """

    sig_service_updated = Signal(object, str, str)
    """
    TODO:

    Parameters
    ----------
    zeroconf: ServiceInfo
        TODO:
    service_type: str
        TODO:
    name: str
        TODO:
    """

    def __init__(self):
        super().__init__()

    def add_service(self, zeroconf_instance, service_type, name):
        super().add_service(zeroconf_instance, service_type, name)
        self.sig_service_added.emit(zeroconf_instance, service_type, name)

    def remove_service(self, zeroconf_instance, service_type, name):
        super().remove_service(zeroconf_instance, service_type, name)
        self.sig_service_removed.emit(zeroconf_instance, service_type, name)

    def update_service(self, zeroconf_instance, service_type, name):
        super().update_service(zeroconf_instance, service_type, name)
        self.sig_service_updated.emit(zeroconf_instance, service_type, name)
