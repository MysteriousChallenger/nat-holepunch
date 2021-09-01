from abc import ABC, abstractmethod
from typing import Callable

from ..package import Package


class AbstractPackageSocket(ABC):
    def __init__(self, **kwargs):
        self.is_open = True
        pass

    @abstractmethod
    def send(self, package: Package) -> None:
        raise NotImplementedError

    @abstractmethod
    def recv(self) -> Package:
        raise NotImplementedError

    def close(self):
        self.is_open = False


class PackageSocketShutdownException(Exception):
    pass
