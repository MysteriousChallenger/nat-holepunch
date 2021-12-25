from functools import wraps
from typing import Callable

from util.threading import Thread, TimeoutException
from util.typing import P

from .AbstractHandler import PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE, AbstractHandler


class AbstractTimeoutHandler(AbstractHandler[PAYLOAD_TYPE, RESPONSE_TYPE, CONTEXT_TYPE]):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.handle_request = cls._wrap_timeout(cls.handle_request)

    def __init__(self, timeout: float = None, default: PAYLOAD_TYPE = None, **kwargs):
        super().__init__(**kwargs)
        self.timeout = timeout
        self.default = default

    @staticmethod
    def _wrap_timeout(
        handle_request: Callable[P, RESPONSE_TYPE]
    ) -> Callable[P, RESPONSE_TYPE]:

        if (
            hasattr(handle_request, "_AbstractTimeoutHandler_wrapped")
            and handle_request._AbstractTimeoutHandler_wrapped == True
        ):
            return handle_request

        @wraps(handle_request)
        def execute_with_timeout(self: "AbstractTimeoutHandler") -> RESPONSE_TYPE:
            result = None
            completed = False

            def run_execute_and_store_result():
                nonlocal result
                nonlocal completed
                try:
                    result = handle_request()
                    completed = True
                except TimeoutException:
                    pass

            thread = Thread(target=run_execute_and_store_result, daemon=True)
            thread.start()
            thread.join(self.timeout)

            if not completed:
                result = self.default

            return result  # type: ignore

        execute_with_timeout._AbstractTimeoutHandler_wrapped = True

        return execute_with_timeout
