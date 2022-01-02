from abc import abstractmethod
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

import protocol

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

class PackageSocketRequestServer(AbstractRequestServer[SerializableType, SerializableType, CONTEXT_TYPE]):
    def __init__(self, socket: GeneralPurposeSocket):
        super().__init__()

        self.is_alive = True

        self.request_socket: GeneralPurposeSocket[
            RequestPackage[SerializableType]
        ] = socket.duplicate(filter=lambda x: socket.filter(x) and PackageSocketRequestServer.is_request(x))
        
        self.init_request_handlers()

        self.request_handler_thread = self.start_request_handler_thread()

    def get_request(self) -> RequestData[SerializableType]:
        request_package = self.request_socket.recv()
        if isinstance(request_package, RequestPackage):
            type = request_package._type
            payload = request_package.payload
            uuid = request_package._uuid

            return RequestData(type, payload, uuid)
        raise Exception

    def dispatch_response(
        self, request: RequestData[SerializableType], response
    ) -> None:
        response_package = ResponsePackage(response, request.id)
        self.request_socket.send(response_package)

    def start_request_handler_thread(self) -> Thread:
        def request_handler_loop():
            try:
                self.serve()
            except PackageSocketShutdownException:
                self.is_alive = False

        handler_thread = Thread(target=request_handler_loop, daemon=True)
        handler_thread.start()
        return handler_thread

    def init_request_handlers(self):
        handlers = list(
            i(context = self.get_context()) for i in AbstractSerializableHandler[CONTEXT_TYPE]._handler_types.values()
        )
        self.register_handler(*handlers)

    @abstractmethod
    def get_context(self) -> CONTEXT_TYPE:
        raise NotImplementedError

    def shutdown(self):
        self.request_socket.close()
        self.wait_until_termination()

    def detach(self):
        self.request_handler_thread.join(0)
        self.wait_until_termination()

    def wait_until_termination(self):
        self.request_handler_thread.join()
        self.is_alive = False


    @staticmethod
    def is_request(package: Package):
        return isinstance(package, RequestPackage)