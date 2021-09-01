import inspect
from typing import Dict, Type

from jsonIO import SerializableType

from .AbstractHandler import AbstractHandler


class AbstractSerializableHandler(AbstractHandler[SerializableType, SerializableType]):

    _handler_types: Dict[
        str, Type[AbstractHandler[SerializableType, SerializableType]]
    ] = dict()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if inspect.isabstract(cls):
            return

        if cls.TYPE is NotImplemented:
            cls.TYPE = cls.__name__

        if cls.TYPE in AbstractSerializableHandler._handler_types:
            raise TypeError(
                f'Request type "{cls.TYPE}" declared by {cls.__name__} is already in use by {AbstractSerializableHandler._handler_types[cls.TYPE].__name__}'
            )

        AbstractSerializableHandler._handler_types[cls.TYPE] = cls
