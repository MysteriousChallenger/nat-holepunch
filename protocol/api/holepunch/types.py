
from typing import List, Tuple, TypedDict

addr_type = Tuple[str, int]

class RegisterClientRequestPayload(TypedDict):
    name: str
    addr: addr_type

class ConnectToPeerRequestPayload(TypedDict):
    peer_name: str
    client_name: str
    return_addrs: List[addr_type]