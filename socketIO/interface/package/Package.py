from typing import Generic, TypeVar

from typing_extensions import TypeGuard

from jsonIO import Serializable, SerializableTypeVar

PackageType = TypeVar("PackageType", bound="Package")


class Package(Generic[SerializableTypeVar], Serializable):
    def __init__(self, payload: SerializableTypeVar):
        self.payload = payload

    @classmethod
    def from_json(cls, json: dict) -> "Package":
        return cls(**json)

    def to_json(self) -> dict:
        return self.__dict__


class NullPackageType(Package):
    def __init__(self):
        super().__init__(None)

    @staticmethod
    def is_null_package(package: Package) -> TypeGuard["NullPackageType"]:
        return isinstance(package, NullPackageType)


NullPackage = NullPackageType()
