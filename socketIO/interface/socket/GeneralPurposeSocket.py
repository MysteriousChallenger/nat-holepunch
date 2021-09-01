from typing import Callable, Generic

from ..package import Package, PackageType
from .DuplicableSocket import DuplicableSocket
from .FilteredSocket import FilteredSocket


class GeneralPurposeSocket(FilteredSocket, DuplicableSocket, Generic[PackageType]):
    def __init__(
        self,
        _underlying: DuplicableSocket = None,
        filter: Callable[[Package], bool] = lambda _: True,
        **kwargs
    ):
        super().__init__(_underlying=_underlying, filter=filter, **kwargs)
