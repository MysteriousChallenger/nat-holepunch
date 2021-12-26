import inspect
from typing import Any, ClassVar, Dict, Generic, Type

from jsonIO import SerializableType

from .AbstractExecutableRequest import (
    CONTEXT_TYPE,
    RESULT_TYPE,
    AbstractExecutableRequest,
)


class AbstractSerializableRequest(
    AbstractExecutableRequest[SerializableType, SerializableType, RESULT_TYPE, CONTEXT_TYPE]
):
    TYPE: ClassVar[str] = NotImplemented
    _request_types: Dict[str, Type["AbstractSerializableRequest[RESULT_TYPE, CONTEXT_TYPE]"]] = dict()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)

        if inspect.isabstract(cls):
            return

        if cls.TYPE is NotImplemented:
            cls.TYPE = cls.__name__

        if cls.TYPE in AbstractSerializableRequest._request_types:
            raise TypeError(
                f'Request type "{cls.TYPE}" declared by {cls.__name__} is already in use by {AbstractSerializableRequest._request_types[cls.TYPE].__name__}'
            )

        AbstractSerializableRequest._request_types[cls.TYPE] = cls
