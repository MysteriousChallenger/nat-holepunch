from functools import wraps
from typing import Callable

from util.typing import P

from ..package import NullPackage, Package
from .ThreadSafeSocket import ThreadSafeSocket


class FilteredSocket(ThreadSafeSocket):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.recv = FilteredSocket.wrap_recv(cls.recv)

    def __init__(self, filter: Callable[[Package], bool] = lambda _: True, **kwargs):
        super().__init__(**kwargs)
        self.filter = filter

    @staticmethod
    def wrap_recv(recv_func: Callable[P, Package]) -> Callable[P, Package]:

        if (
            hasattr(recv_func, "_FilteredSocket_wrapped")
            and recv_func._FilteredSocket_wrapped == True
        ):
            return recv_func

        @wraps(recv_func)
        def recv(self: "FilteredSocket"):
            while True:
                package = recv_func(self)  # type: ignore
                if self.filter(package) or package is NullPackage:
                    return package

        recv._FilteredSocket_wrapped = True

        return recv
