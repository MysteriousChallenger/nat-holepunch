import collections
from functools import wraps
from threading import Condition, Event, Lock, RLock
from typing import Callable, Generic, Set

from util.threading import QLock
from util.typing import P

from ..package import Package
from .AbstractPackageSocket import PackageSocketShutdownException
from .ThreadSafeSocket import ThreadSafeSocket


class DuplicableSocket(ThreadSafeSocket):
    def __init_subclass__(cls) -> None:
        super(ThreadSafeSocket, cls).__init_subclass__()
        cls.send = DuplicableSocket.wrap_send(cls.send)
        cls.recv = DuplicableSocket.wrap_recv(cls.recv)

    def __init__(self, _underlying: "DuplicableSocket" = None, **kwargs):
        super().__init__(**kwargs)
        if _underlying == None:
            self._underlying = self
            self.duplicates: Set[DuplicableSocket] = set()
            self._duplicate_lock = RLock()
            self._check_buffer_event = Condition()
        else:
            self._underlying = _underlying
            self.duplicates = _underlying.duplicates
            self._duplicate_lock = _underlying._duplicate_lock
            self._check_buffer_event = _underlying._check_buffer_event

        self.buf = collections.deque()
        self.duplicates.add(self)

    def __del__(self):
        if hasattr(self, "duplicates"):
            self.duplicates.remove(self)

        if hasattr(super(), "__del__"):
            super().__del__()  # type: ignore

    @staticmethod
    def wrap_send(send_func: Callable[P, None]) -> Callable[P, None]:

        if (
            hasattr(send_func, "_DuplicableSocket_wrapped")
            and send_func._DuplicableSocket_wrapped == True
        ):
            return send_func

        @wraps(send_func)
        def send(self: "DuplicableSocket", package: Package) -> None:
            if self._underlying == self:
                send_func(self, package)  # type: ignore
            else:
                self._underlying.send(package)

        send._DuplicableSocket_wrapped = True

        return send

    @staticmethod
    def wrap_recv(recv_func: Callable[P, Package]) -> Callable[P, Package]:

        if (
            hasattr(recv_func, "_DuplicableSocket_wrapped")
            and recv_func._DuplicableSocket_wrapped == True
        ):
            return recv_func

        @wraps(recv_func)
        def recv(self: "DuplicableSocket") -> Package:
            while True:
                # if buffer contains packages, recieve those first
                if len(self.buf) != 0:
                    return self.buf.popleft()

                # if can acquire lock, recv next package and add it to all duplicates' buffers
                if self._duplicate_lock.acquire(blocking=False):
                    try:
                        with self._duplicate_lock:
                            self._duplicate_lock.release()

                            package = recv_func(self)  # type: ignore
                            for duplicate in self.duplicates:
                                duplicate._buf_append(package)

                            # notify other duplicates that a package is available
                            with self._check_buffer_event:
                                self._check_buffer_event.notify_all()

                            return_value = self.buf.popleft()
                            return return_value

                    except PackageSocketShutdownException:
                        # notify other duplicates since otherwise they would be waiting for the leading thread to notify them
                        with self._check_buffer_event:
                            self._check_buffer_event.notify_all()
                        raise

                # await notification that a package is available
                with self._check_buffer_event:
                    self._check_buffer_event.wait()
                    if len(self.buf) != 0:
                        return self.buf.popleft()

        recv._DuplicableSocket_wrapped = True

        return recv

    def _buf_append(self, package: Package):
        self.buf.append(package)

    def duplicate(self, **kwargs):
        return self.__class__(**{**self.__dict__, **kwargs})
