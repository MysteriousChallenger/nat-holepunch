from functools import wraps
from typing import Any, Callable

from util.threading import Thread
from util.typing import P

from .AbstractExecutableRequest import RESULT_TYPE, AbstractExecutableRequest


class AbstractTimeOutRequest(AbstractExecutableRequest[Any, Any, Any]):
    @classmethod
    def __init_subclass_(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        cls.execute = cls._wrap_execute(cls.execute)

    def __init__(self, timeout: float, default: RESULT_TYPE, **kwargs):
        super().__init__(**kwargs)
        self.timeout = timeout
        self.default = default

    @staticmethod
    def _wrap_execute(execute_fn: Callable[P, RESULT_TYPE]) -> Callable[P, RESULT_TYPE]:

        if (
            hasattr(execute_fn, "_AbstractTimeOutRequest_wrapped")
            and execute_fn._AbstractTimeOutRequest_wrapped == True
        ):
            return execute_fn

        @wraps(execute_fn)
        def execute_with_timeout(self: "AbstractTimeOutRequest") -> RESULT_TYPE:  # type: ignore
            result = None
            completed = False

            def run_execute_and_store_result():
                nonlocal result
                nonlocal completed
                result = execute_fn()
                completed = True

            thread = Thread(target=run_execute_and_store_result, daemon=True)
            thread.start()
            thread.join(self.timeout)

            if not completed:
                result = self.default

            return result  # type: ignore

        execute_fn._AbstractTimeOutRequest_wrapped = True

        return execute_with_timeout
