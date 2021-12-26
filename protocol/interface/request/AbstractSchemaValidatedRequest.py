import functools
import inspect
from typing import Any, Callable

import jsonschema

from util.typing import P

from .AbstractExecutableRequest import (
    CONTEXT_TYPE,
    PAYLOAD_TYPE,
    RESPONSE_TYPE,
    RESULT_TYPE,
    AbstractExecutableRequest,
)


class AbstractSchemaValidatedRequest(AbstractExecutableRequest[PAYLOAD_TYPE, RESPONSE_TYPE, RESULT_TYPE, CONTEXT_TYPE]):

    PAYLOAD_SCHEMA = NotImplemented
    RESPONSE_SCHEMA = NotImplemented

    @classmethod
    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        if cls.PAYLOAD_SCHEMA is NotImplemented and not inspect.isabstract(cls):
            raise NotImplementedError(f"{cls.__name__}.payload_schema is not defined")

        if cls.RESPONSE_SCHEMA is NotImplemented and not inspect.isabstract(cls):
            raise NotImplementedError(f"{cls.__name__}.response_schema is not defined")

        cls.prepare_payload = AbstractSchemaValidatedRequest._wrap_prepare_payload(
            cls.prepare_payload, cls._validate_payload
        )
        cls.process_response = AbstractSchemaValidatedRequest._wrap_process_response(
            cls.process_response, cls._validate_response
        )

    @classmethod
    def _validate_payload(cls, payload: Any) -> None:
        return jsonschema.validate(payload, cls.PAYLOAD_SCHEMA)

    @classmethod
    def _validate_response(cls, response: Any) -> None:
        return jsonschema.validate(response, cls.RESPONSE_SCHEMA)

    @staticmethod
    def _wrap_prepare_payload(
        prepare_payload: Callable[P, PAYLOAD_TYPE],
        validate_payload: Callable[[PAYLOAD_TYPE], None],
    ) -> Callable[P, PAYLOAD_TYPE]:

        if (
            hasattr(prepare_payload, "_AbstractSchemaValidatedRequest_wrapped")
            and prepare_payload._AbstractSchemaValidatedRequest_wrapped == True
        ):
            return prepare_payload

        @functools.wraps(prepare_payload)
        def prepare_and_validate(
            self: "AbstractSchemaValidatedRequest",
        ) -> PAYLOAD_TYPE:
            payload = prepare_payload(self)  # type: ignore
            validate_payload(payload)
            return payload

        prepare_and_validate._AbstractSchemaValidatedRequest_wrapped = True

        return prepare_and_validate

    @staticmethod
    def _wrap_process_response(
        process_response: Callable[P, RESULT_TYPE],
        validate_response: Callable[[RESPONSE_TYPE], None],
    ) -> Callable[P, RESULT_TYPE]:

        if (
            hasattr(process_response, "_AbstractSchemaValidatedRequest_wrapped")
            and process_response._AbstractSchemaValidatedRequest_wrapped == True
        ):
            return process_response

        @functools.wraps(process_response)
        def validate_and_process(
            self: "AbstractSchemaValidatedRequest", response: RESPONSE_TYPE
        ) -> RESULT_TYPE:
            validate_response(response)
            result = process_response(self, response)  # type: ignore
            return result

        validate_and_process._AbstractSchemaValidatedRequest_wrapped = True

        return validate_and_process
