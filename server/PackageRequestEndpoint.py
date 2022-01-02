import threading
from types import MethodType
from typing import Any, Dict, Generic, NoReturn

from jsonIO.Serializable import SerializableType
from protocol.interface import (
    AbstractRequestClient,
    AbstractRequestServer,
    AbstractSerializableHandler,
    AbstractSerializableRequest,
    CONTEXT_TYPE,
    Promise,
    RequestData,
    request,
)
from socketIO import (
    GeneralPurposeSocket,
    NullPackageType,
    Package,
    RequestPackage,
    ResponsePackage,
)
from socketIO.interface.socket.AbstractPackageSocket import (
    PackageSocketShutdownException,
)
from util.threading import Thread

from .PackageSocketRequestClient import PackageSocketRequestClient
from .PackageSocketRequestServer import PackageSocketRequestServer

class PackageRequestEndpoint(
    PackageSocketRequestClient[CONTEXT_TYPE],
    PackageSocketRequestServer[CONTEXT_TYPE]
):
    def __init__(self, socket: GeneralPurposeSocket, **kwargs):
        PackageSocketRequestServer.__init__(self, socket = socket, **kwargs)
        PackageSocketRequestClient.__init__(self, socket = socket, **kwargs)
        self.is_alive = True

    def shutdown(self):
        PackageSocketRequestClient.shutdown(self)
        PackageSocketRequestServer.shutdown(self)
        self.is_alive = False

    def detach(self):
        PackageSocketRequestClient.detach(self)
        PackageSocketRequestServer.detach(self)
        self.is_alive = False

    def wait_until_termination(self):
        PackageSocketRequestClient.wait_until_termination(self)
        PackageSocketRequestServer.wait_until_termination(self)
        self.is_alive = False