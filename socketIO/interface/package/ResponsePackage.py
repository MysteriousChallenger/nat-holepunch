import uuid
from typing import Generic

from typing_extensions import TypeGuard

from jsonIO import Serializable, SerializableTypeVar

from .Package import Package


class ResponsePackage(Package[SerializableTypeVar], Generic[SerializableTypeVar]):
    def __init__(self, payload: SerializableTypeVar, _uuid: int):
        super().__init__(payload)
        self._uuid = _uuid or uuid.uuid4().int

    @staticmethod
    def is_response_package(package: Package) -> TypeGuard["ResponsePackage"]:
        return isinstance(package, ResponsePackage)
