from collections import deque
from contextlib import AbstractContextManager
from threading import Lock
from types import TracebackType
from typing import Deque, Type


class QLock(AbstractContextManager):
    def __init__(self):
        super().__init__()
        self.queue: Deque[Lock] = deque()
        self.lock = Lock()

    def __enter__(self) -> "QLock":
        self.acquire()
        return self

    def __exit__(self, __exc_type, __exc_value, traceback):
        self.release()

    def acquire(self, blocking: bool = True) -> bool:
        if len(self.queue) == 0 and not self.lock.locked():
            return self.lock.acquire(blocking=blocking)

        queue_lock = Lock()
        self.queue.append(queue_lock)

        # lock this thread until the queue lock is released
        queue_lock.acquire()
        queue_lock.acquire()

        # acquire main lock, release queue lock
        result = self.lock.acquire(blocking=blocking)
        queue_lock.release()
        return result

    def release(self) -> None:
        if len(self.queue) == 0:
            return self.lock.release()

        self.queue[0].release()
        result = self.lock.release()
        self.queue.pop()
        return result
