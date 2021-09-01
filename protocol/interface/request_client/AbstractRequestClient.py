from abc import ABC, abstractmethod
from threading import Event
from typing import Generic, TypeVar, Union

T = TypeVar("T")
PAYLOAD_TYPE = TypeVar("PAYLOAD_TYPE")
RESPONSE_TYPE = TypeVar("RESPONSE_TYPE")
RESULT_TYPE = TypeVar("RESULT_TYPE")


class Promise(Event, Generic[T]):
    def __init__(self, default: T = None):
        super().__init__()
        self.value: Union[T, None] = default
        self.default = default

    def wait(self, timeout: float = None, default: T = None):
        self.default = default
        if super().wait(timeout=timeout):
            return self.value
        else:
            return self.default

    def set(self, value: Union[T, None]):
        if value == None:
            value = self.default
        self.value = value
        super().set()


class AbstractRequestClient(ABC, Generic[PAYLOAD_TYPE, RESPONSE_TYPE]):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def dispatch_request(
        self, request_type: str, payload: PAYLOAD_TYPE
    ) -> Promise[RESPONSE_TYPE]:
        raise NotImplementedError
