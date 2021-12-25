from typing import Generic, NamedTuple, TypeVar

PAYLOAD_TYPE = TypeVar("PAYLOAD_TYPE")

class RequestDataBASE(NamedTuple):
    type: str
    payload: PAYLOAD_TYPE  # type: ignore
    id: int


class RequestData(RequestDataBASE, Generic[PAYLOAD_TYPE]):
    type: str
    payload: PAYLOAD_TYPE  # type: ignore
    id: int
