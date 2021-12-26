
from typing import Tuple, TypedDict
class RegisterClientRequestPayload(TypedDict):
    name: str
    addr: Tuple[str, int]