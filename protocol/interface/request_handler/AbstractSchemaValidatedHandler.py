import functools
import inspect
from typing import Callable

import jsonschema

from util.typing import P

from ..request import RequestData
from .AbstractHandler import PAYLOAD_TYPE, RESPONSE_TYPE, AbstractHandler


class AbstractSchemaValidatedHandler(AbstractHandler[PAYLOAD_TYPE, RESPONSE_TYPE]):

    _payload_schema = NotImplemented
    _response_schema = NotImplemented

    @classmethod
    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        if cls._payload_schema is NotImplemented and not inspect.isabstract(cls):
            raise NotImplementedError(f"{cls.__name__}.payload_schema is not defined")

        if cls._response_schema is NotImplemented and not inspect.isabstract(cls):
            raise NotImplementedError(f"{cls.__name__}.response_schema is not defined")

        cls.process_request = AbstractSchemaValidatedHandler._wrap_process_request(
            cls.process_request, cls._validate_payload, cls._validate_response
        )

    @staticmethod
    def _wrap_process_request(
        process_request: Callable[P, RESPONSE_TYPE],
        validate_payload: Callable[[PAYLOAD_TYPE], None],
        validate_response: Callable[[RESPONSE_TYPE], None],
    ) -> Callable[P, RESPONSE_TYPE]:

        if (
            hasattr(process_request, "_AbstractSchemaValidatedHandler_wrapped")
            and process_request._AbstractSchemaValidatedHandler_wrapped == True
        ):
            return process_request

        @functools.wraps(process_request)
        def validate_and_process(self, request: RequestData[PAYLOAD_TYPE]):
            validate_payload(request.payload)
            response = process_request(self, request)  # type: ignore
            validate_response(response)
            return response

        validate_and_process._AbstractSchemaValidatedHandler_wrapped = True

        return validate_and_process

    @classmethod
    def _validate_payload(cls, payload: PAYLOAD_TYPE):
        return jsonschema.validate(payload, cls._payload_schema)

    @classmethod
    def _validate_response(cls, response: RESPONSE_TYPE):
        return jsonschema.validate(response, cls._response_schema)
