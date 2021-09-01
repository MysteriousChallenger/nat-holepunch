import threading
from types import MethodType
from typing import Dict, NoReturn

from jsonIO.Serializable import SerializableType
from protocol.interface import (
    AbstractRequestClient,
    AbstractRequestServer,
    AbstractSerializableHandler,
    AbstractSerializableRequest,
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


class PackageRequestEndpoint(
    AbstractRequestClient[SerializableType, SerializableType],
    AbstractRequestServer[SerializableType, SerializableType],
):
    def __init__(self, socket: GeneralPurposeSocket):
        super(AbstractRequestClient, self).__init__()
        super(AbstractRequestServer, self).__init__()

        self.is_alive = True

        self.request_socket: GeneralPurposeSocket[
            RequestPackage[SerializableType]
        ] = socket.duplicate(filter=lambda x: socket.filter(x) and self.is_request(x))
        self.response_socket: GeneralPurposeSocket[
            ResponsePackage[SerializableType]
        ] = socket.duplicate(filter=lambda x: socket.filter(x) and self.is_response(x))

        self.pending_requests: Dict[int, Promise[SerializableType]] = dict()

        self.init_request_handlers()
        self.init_requests()

        self.response_handler_thread = self.start_response_handler_thread()
        self.request_handler_thread = self.start_request_handler_thread()

    def dispatch_request(
        self, request_type: str, payload: SerializableType
    ) -> Promise[SerializableType]:

        request = RequestPackage(payload, request_type)
        uuid = request._uuid
        promise = Promise()

        # add request to pending dict
        self.pending_requests[uuid] = promise

        # send actual request
        self.response_socket.send(request)

        # promise will be resolved when we recieve a notification from response handler thread
        return promise

    def start_response_handler_thread(self) -> Thread:
        def handle_response(response_package: Package):  # type: ignore
            if isinstance(response_package, ResponsePackage):
                uuid = response_package._uuid
                response = response_package.payload
                if uuid not in self.pending_requests:
                    raise Exception("got response for nonexistent request id {uuid}")
                self.pending_requests[uuid].set(response)
            elif isinstance(response_package, NullPackageType):
                pass
            else:
                raise Exception(
                    f"cant handle non response package {response_package} of type {response_package.__class__}"
                )

        def handler_loop():
            try:
                while True:
                    response_package = self.response_socket.recv()
                    handle_response(response_package)
            except PackageSocketShutdownException:
                for promise in self.pending_requests.values():
                    promise.set(None)
                self.alive = False

        handler_thread = Thread(target=handler_loop, daemon=True)
        handler_thread.start()
        return handler_thread

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
        self.response_socket.send(response_package)

    def start_request_handler_thread(self) -> Thread:
        def request_handler_loop():
            try:
                self.serve()
            except PackageSocketShutdownException:
                self.alive = False

        handler_thread = Thread(target=request_handler_loop, daemon=True)
        handler_thread.start()
        return handler_thread

    def init_request_handlers(self):
        handlers = list(
            i() for i in AbstractSerializableHandler._handler_types.values()
        )
        self.register_handler(*handlers)

    def init_requests(self):
        requests = list(AbstractSerializableRequest._request_types.values())
        for request in requests:

            def init_and_run_request(self, client=None, *args, **kwargs):
                if client == None:
                    client = self
                request_instance = request(client=client, *args, **kwargs)
                return request_instance.execute()

            setattr(self, request.TYPE, MethodType(init_and_run_request, self))

    def shutdown(self):
        self.request_socket.close()
        self.response_socket.close()
        self.request_handler_thread.join(0)
        self.response_handler_thread.join(0)
        self.alive = False

    def wait_until_termination(self):
        self.request_handler_thread.join()
        self.response_handler_thread.join()
        self.alive = False

    def __type_hinting__(self):
        requests = list(AbstractSerializableRequest._request_types.values())
        for request in requests:

            def init_and_run_request(self, client=None, *args, **kwargs):
                if client == None:
                    client = self
                request_instance = request(client, *args, **kwargs)
                return request_instance.execute()

            setattr(self, request.TYPE, MethodType(init_and_run_request, self))

    @staticmethod
    def is_request(package: Package):
        return isinstance(package, RequestPackage)

    @staticmethod
    def is_response(package: Package):
        return isinstance(package, ResponsePackage)
