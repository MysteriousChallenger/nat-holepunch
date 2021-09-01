import uuid
from typing import Generic

from typing_extensions import TypeGuard

from jsonIO import Serializable, SerializableTypeVar

from .Package import Package


class RequestPackage(Package[SerializableTypeVar], Generic[SerializableTypeVar]):
    def __init__(self, payload: SerializableTypeVar, _type: str, _uuid: int = None):
        super().__init__(payload)
        self._uuid = _uuid or uuid.uuid4().int
        self._type = _type

    @staticmethod
    def is_request_package(package: Package) -> TypeGuard["RequestPackage"]:
        return isinstance(package, RequestPackage)
