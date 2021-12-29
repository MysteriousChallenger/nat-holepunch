from typing import List, Tuple

from protocol.interface import (
    AbstractSerializableHandler,
    RequestData,
)
from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext

from .context_descriptors import ClientAddressDict, ClientDict, ClientName
from .types import RegisterClientRequestPayload, addr_type


class RegisterClientHandler(AbstractSerializableHandler[TCPPackageRequestServerContext]):

    TYPE = 'register_client'

    client_address = ClientAddressDict()
    clients = ClientDict()
    name = ClientName()

    def process_request(self, request: RequestData[RegisterClientRequestPayload]) -> Tuple[bool, List[addr_type]]:
        if request.payload['name'] in self.client_address:
            return False, []

        if self.name != None:
            del self.client_address[self.name]
            del self.clients[self.name]

        name = request.payload['name']
        priv_addr = request.payload['addr']
        pub_addr = self.context.endpoint.socket._tcp_socket.getpeername()

        self.name = name
        self.client_address[name] = [priv_addr, pub_addr]
        self.clients[name] = self.context.endpoint

        return True, [priv_addr, pub_addr]

    def __del__(self):
        if self.name != None:
            del self.client_address[self.name]
            del self.clients[self.name]