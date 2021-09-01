import inspect
from abc import ABC, abstractmethod
from typing import ClassVar, Dict, Final, Generic, Type, TypeVar

from ..request_client import AbstractRequestClient

PAYLOAD_TYPE = TypeVar("PAYLOAD_TYPE")
RESPONSE_TYPE = TypeVar("RESPONSE_TYPE")
RESULT_TYPE = TypeVar("RESULT_TYPE")


class AbstractExecutableRequest(ABC, Generic[PAYLOAD_TYPE, RESPONSE_TYPE, RESULT_TYPE]):

    TYPE: ClassVar[str] = NotImplemented
    _request_types: Dict[str, Type["AbstractExecutableRequest"]] = dict()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if inspect.isabstract(cls):
            return

        if cls.TYPE is NotImplemented:
            cls.TYPE = cls.__name__

        if cls.TYPE in AbstractExecutableRequest._request_types:
            raise TypeError(
                f'Request type "{cls.TYPE}" declared by {cls.__name__} is already in use by {AbstractExecutableRequest._request_types[cls.TYPE].__name__}'
            )

        else:
            AbstractExecutableRequest._request_types[cls.TYPE] = cls

    def __init__(
        self, client: AbstractRequestClient[PAYLOAD_TYPE, RESPONSE_TYPE], **kwargs
    ):
        self.client = client

    def execute(self):
        payload = self.prepare_payload()
        response = self.dispatch_request(payload)
        return self.process_response(response)

    @abstractmethod
    def prepare_payload(self) -> PAYLOAD_TYPE:
        raise NotImplementedError

    def dispatch_request(self, payload: PAYLOAD_TYPE):
        promise = self.client.dispatch_request(self.TYPE, payload)
        response = promise.wait()
        return response

    @abstractmethod
    def process_response(self, response: RESPONSE_TYPE) -> RESULT_TYPE:
        raise NotImplementedError
