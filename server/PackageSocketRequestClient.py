from abc import abstractmethod
from weakref import proxy
from types import MethodType
from typing import Dict, Generic
from functools import wraps
import concurrent.futures

from jsonIO.Serializable import SerializableType
from protocol.interface import (
    AbstractRequestClient,
    AbstractSerializableRequest,
    CONTEXT_TYPE,
    Promise,
)
from socketIO import (
    GeneralPurposeSocket,
    NullPackageType,
    Package,
    PackageSocketShutdownException,
    RequestPackage,
    ResponsePackage,
)
from util.threading import Thread

class PackageSocketRequestClient(AbstractRequestClient[SerializableType, SerializableType], Generic[CONTEXT_TYPE]):
    def __init__(self, socket: GeneralPurposeSocket, **kwargs):
        super(PackageSocketRequestClient, self).__init__()
        
        self.is_alive = True

        self.response_socket: GeneralPurposeSocket[
            ResponsePackage[SerializableType]
        ] = socket.duplicate(filter=lambda x: socket.filter(x) and PackageSocketRequestClient.is_response(x))

        self.pending_requests: Dict[int, Promise[SerializableType]] = dict()

        self.init_requests()

        self.response_handler_thread = self.start_response_handler_thread()

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
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    while True:
                        response_package = self.response_socket.recv()
                        executor.submit(handle_response, response_package)
            except PackageSocketShutdownException:
                for promise in self.pending_requests.values():
                    promise.set(None)
                self.is_alive = False

        handler_thread = Thread(target=handler_loop, daemon=True)
        handler_thread.start()
        return handler_thread

    @abstractmethod
    def get_context(self) -> CONTEXT_TYPE:
        raise NotImplementedError

    def init_requests(self):
        requests = list(AbstractSerializableRequest._request_types.values())

        def request_factory(request):

            @wraps(request.__init__)
            def init_and_run_request(self, *args, **kwargs):
                request_instance = request(client=self, context=self.get_context(), *args, **kwargs)
                return request_instance.execute()
            
            return init_and_run_request

        for request in requests:
            setattr(self, request.TYPE, MethodType(request_factory(request), proxy(self)))

    def shutdown(self):
        self.response_socket.close()
        self.wait_until_termination()

    def detach(self):
        self.response_handler_thread.join(0)
        self.wait_until_termination()

    def wait_until_termination(self):
        self.response_handler_thread.join()
        self.is_alive = False

    @staticmethod
    def is_response(package: Package):
        return isinstance(package, ResponsePackage)
