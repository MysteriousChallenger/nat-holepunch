from __future__ import annotations

import abc
from typing import Dict, List, TypeVar, Union


class Serializable(abc.ABC):
    serializable_classes = []

    def __init_subclass__(cls) -> None:
        cls.serializable_classes.append(cls)

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json: dict) -> Serializable:
        raise NotImplementedError

    @abc.abstractmethod
    def to_json(self) -> dict:
        raise NotImplementedError


SerializableType = Union[
    List["SerializableType"],
    Dict["SerializableType", "SerializableType"],
    Serializable,
    None,
    bool,
    str,
    float,
    int,
]

SerializableTypeVar = TypeVar("SerializableTypeVar", bound=SerializableType)
