from functools import wraps
from threading import Lock
from typing import Callable

from typing_extensions import ParamSpec

from ..package import Package
from .AbstractPackageSocket import AbstractPackageSocket

P = ParamSpec("P")


class ThreadSafeSocket(AbstractPackageSocket):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.send = ThreadSafeSocket.wrap_send(cls.send)
        cls.recv = ThreadSafeSocket.wrap_recv(cls.recv)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send_lock = Lock()
        self.recv_lock = Lock()

    @staticmethod
    def wrap_send(send_func: Callable[P, None]) -> Callable[P, None]:
        @wraps(send_func)
        def send(self, package: Package):
            with self.send_lock:
                send_func(self, package)  # type: ignore

        return send

    @staticmethod
    def wrap_recv(recv_func: Callable[P, Package]) -> Callable[P, Package]:
        @wraps(recv_func)
        def recv(self):
            with self.recv_lock:
                return recv_func(self)  # type: ignore

        return recv
