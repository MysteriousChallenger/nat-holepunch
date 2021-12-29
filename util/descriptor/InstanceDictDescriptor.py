from typing import Dict, Generic, TypeVar

from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext
from util.typing import T

from .attr import rgetattr


class InstanceDictDescriptor(Generic[T], object):
    def __init__(self, dict: str, key, default: T = None) -> None:
        self.dict = dict
        self.key = key
        self.default = default

    def __get__(self, obj, objtype=None) -> T:
        dict = rgetattr(obj,self.dict)
        if self.key not in dict:
            dict[self.key] = self.default

        return dict[self.key]

    def __set__(self, obj, value: T):
        rgetattr(obj,self.dict)[self.key] = value