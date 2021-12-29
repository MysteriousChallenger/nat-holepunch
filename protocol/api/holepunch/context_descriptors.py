from typing import List, Tuple, Union

from server import TCPPackageRequestServerContext
from util import InstanceDictDescriptor

from .types import addr_type

#   Context descriptors pretend to be instance variables but can share a value across
# all handlers and requests who also share the same context.

class ClientAddressDict(InstanceDictDescriptor[dict]):
    def __init__(self) -> None:
        super().__init__('context.server_context', 'holepunch_client_addresses', dict())

class ClientDict(InstanceDictDescriptor[dict]):
    def __init__(self) -> None:
        super().__init__('context.server_context', 'holepunch_clients', dict())

class ClientName(InstanceDictDescriptor[Union[str,None]]):
    def __init__(self) -> None:
        super().__init__('context.endpoint_context', 'holepunch_client_name', None)

class RegisteredName(InstanceDictDescriptor[Union[str,None]]):
    def __init__(self) -> None:
        super().__init__('context.endpoint_context', 'holepunch_registered_name', None)

class RegisteredAddrs(InstanceDictDescriptor[List[addr_type]]):
    def __init__(self) -> None:
        super().__init__('context.endpoint_context', 'holepunch_registered_address', [])

