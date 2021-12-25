import inspect
from abc import ABC, abstractmethod
from typing import ClassVar, Dict, Final, Generic, Type, TypeVar

from ..request.RequestData import RequestData

PAYLOAD_TYPE = TypeVar("PAYLOAD_TYPE")
RESPONSE_TYPE = TypeVar("RESPONSE_TYPE")
CONTEXT_TYPE = TypeVar("CONTEXT_TYPE")


class AbstractHandler(ABC, Generic[PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE]):

    TYPE: ClassVar[str] = NotImplemented
    _handler_types: Dict[str, Type["AbstractHandler"]] = dict()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if inspect.isabstract(cls):
            return

        if cls.TYPE is NotImplemented:
            cls.TYPE = cls.__name__

        if cls.TYPE in AbstractHandler._handler_types:
            raise TypeError(
                f'Request type "{cls.TYPE}" declared by {cls.__name__} is already in use by {AbstractHandler._handler_types[cls.TYPE].__name__}'
            )

        AbstractHandler._handler_types[cls.TYPE] = cls

    def __init__(self, context: CONTEXT_TYPE, **kwargs):
        pass

    @classmethod
    def can_handle(cls, request: RequestData[PAYLOAD_TYPE]):
        return request.type == cls.TYPE

    def handle_request(self, request: RequestData[PAYLOAD_TYPE]):
        if self.can_handle(request):
            return self.process_request(request)
        else:
            raise Exception(
                f"{self} object of class {self.__class__.__name__} and handler type {self} cannot handle request of type {request.type}"
            )

    @abstractmethod
    def process_request(self, request: RequestData[PAYLOAD_TYPE]) -> RESPONSE_TYPE:
        raise NotImplementedError
