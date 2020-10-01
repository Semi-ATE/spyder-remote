# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Spyder Remote zeroconf Qt listener.
"""

from qtpy.QtCore import QObject, Signal

from spyder_remote_client.discover import SpyderRemoteListener


class QSpyderRemoteListener(QObject, SpyderRemoteListener):
    """
    A Zeroconf server listener for spyder-kernels services.

    Connects the SpyderRemoteListener to Qt Signals.
    """

    sig_service_added = Signal(object, str, str)
    """
    This signal is emitted when a zeroconf service is added.

    Parameters
    ----------
    zeroconf_instance: Zeroconf
        The zerconf instance.
    service_type: str
        The service type. Example: '_sdk._tcp.local.'
    name: str
        The name of the host exposing the service.
    """

    sig_service_removed = Signal(object, str, str)
    """
    This signal is emitted when a zeroconf service is removed.

    Parameters
    ----------
    zeroconf_instance: Zeroconf
        The zerconf instance.
    service_type: str
        The service type. Example: '_sdk._tcp.local.'
    name: str
        The name of the host exposing the service.
    """

    sig_service_updated = Signal(object, str, str)
    """
    This signal is emitted when a zeroconf service is updated.

    Parameters
    ----------
    zeroconf_instance: Zeroconf
        The zerconf instance.
    service_type: str
        The service type. Example: '_sdk._tcp.local.'
    name: str
        The name of the host exposing the service.
    """

    def __init__(self):
        super().__init__()

    def add_service(self, zeroconf_instance, service_type, name):
        """
        Handle a zeroconf service addition.

        Parameters
        ----------
        zeroconf_instance: Zeroconf
            The zerconf instance.
        service_type: str
            The service type. Example: '_sdk._tcp.local.'
        name: str
            The name of the host exposing the service.

        Notes
        -----
        This method emits a Qt signal.
        """
        super().add_service(zeroconf_instance, service_type, name)
        self.sig_service_added.emit(zeroconf_instance, service_type, name)

    def remove_service(self, zeroconf_instance, service_type, name):
        """
        Handle a zeroconf service addition.

        Parameters
        ----------
        zeroconf_instance: Zeroconf
            The zerconf instance.
        service_type: str
            The service type. Example: '_sdk._tcp.local.'
        name: str
            The name of the host exposing the service.

        Notes
        -----
        This method emits a Qt signal.
        """
        super().remove_service(zeroconf_instance, service_type, name)
        self.sig_service_removed.emit(zeroconf_instance, service_type, name)

    def update_service(self, zeroconf_instance, service_type, name):
        """
        Handle a zeroconf service addition.

        Parameters
        ----------
        zeroconf_instance: Zeroconf
            The zerconf instance.
        service_type: str
            The service type. Example: '_sdk._tcp.local.'
        name: str
            The name of the host exposing the service.

        Notes
        -----
        This method emits a Qt signal.
        """
        super().update_service(zeroconf_instance, service_type, name)
        self.sig_service_updated.emit(zeroconf_instance, service_type, name)
