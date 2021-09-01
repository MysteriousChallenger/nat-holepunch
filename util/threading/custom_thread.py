import ctypes
import threading
from threading import Thread
from typing import Any, Callable, Iterable, Mapping, Union


class Thread(Thread):
    # Thread that will terminate self if join timeout is overrun

    def __init__(
        self,
        group: None = None,
        target: Callable[..., Any] = None,
        name: str = None,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] = None,
        *,
        daemon: bool = None
    ) -> None:
        def try_target(*args, **kwargs):
            try:
                target(*args, **kwargs)  # type: ignore
            except TimeoutException:
                pass

        if target == None:
            try_target = None  # type: ignore

        super().__init__(
            group=group,
            target=try_target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
        )

    def join(self, timeout: float = None):
        super().join(timeout)
        if self.isAlive():
            # raise exception in thread
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self._get_tid()), ctypes.py_object(TimeoutException)
            )

            super().join(0)

    def _get_tid(self) -> int:  # type: ignore
        if hasattr(self, "_thread_id"):
            return self._thread_id

        for tid, tobj in threading._active.items():  # type: ignore
            if tobj is self:
                self._thread_id = tid
                return tid


class TimeoutException(Exception):
    pass
