from functools import wraps
from typing import Any, Callable

from util.threading import Thread
from util.typing import P

from .AbstractExecutableRequest import CONTEXT_TYPE, PAYLOAD_TYPE, RESPONSE_TYPE, RESULT_TYPE, AbstractExecutableRequest
from ..request_client import AbstractRequestClient

class AbstractTimeOutRequest(AbstractExecutableRequest[PAYLOAD_TYPE, RESPONSE_TYPE, RESULT_TYPE, CONTEXT_TYPE]):
    @classmethod
    def __init_subclass_(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        cls.execute = cls._wrap_execute(cls.execute)

    def __init__(self, timeout: float, default: RESULT_TYPE, client: AbstractRequestClient[PAYLOAD_TYPE, RESPONSE_TYPE], context: CONTEXT_TYPE, **kwargs):
        super().__init__(client=client, context=context, **kwargs)
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
