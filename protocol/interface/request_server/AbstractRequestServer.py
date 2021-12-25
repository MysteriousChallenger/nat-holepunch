from abc import abstractmethod
from typing import Any, Callable, Dict, Generic, NoReturn, Tuple, TypeVar

from ..request import RequestData
from ..request_handler import PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE, AbstractHandler


class AbstractRequestServer(Generic[PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE]):
    def __init__(self, **kwargs):
        self.request_handlers: dict[
            str, AbstractHandler[PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE]
        ] = dict()

    def register_handler(self, *handlers: AbstractHandler[PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE]):
        self.request_handlers = {
            **self.request_handlers,
            **{i.TYPE: i for i in handlers},
        }

    def handle_request(self, request: RequestData[PAYLOAD_TYPE]) -> RESPONSE_TYPE:
        if request.type not in self.request_handlers:
            raise Exception(
                "{self} of class {self.__class__.__name__} cannot handle request of type {request_type}"
            )

        return self.request_handlers[request.type].handle_request(request)

    @abstractmethod
    def get_request(self) -> RequestData[PAYLOAD_TYPE]:
        raise NotImplementedError

    @abstractmethod
    def dispatch_response(self, request: RequestData[PAYLOAD_TYPE], response) -> None:
        raise NotImplementedError

    def serve(self):
        while True:
            request = self.get_request()
            response = self.handle_request(request)
            self.dispatch_response(request, response)
