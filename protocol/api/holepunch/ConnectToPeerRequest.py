from threading import Event
from typing import List, Tuple, Union
import socket
import time
import jsonIO

from protocol.interface import AbstractSerializableRequest, Promise
from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext
from socketIO.TCPPackageSocket import TCPPackageSocket

from .context_descriptors import ClientAddressDict, ClientDict, RegisteredAddrs, RegisteredName
from .types import ConnectToPeerRequestPayload, addr_type
from .holepunch_util import accept_holepunch_socket, get_holepunch_socket

class ConnectToPeerRequest(AbstractSerializableRequest[bool, TCPPackageRequestServerContext]):

    TYPE = 'connect_to_peer'

    client_address = ClientAddressDict()
    clients = ClientDict()
    name = RegisteredName()
    addrs = RegisteredAddrs()

    def __init__(self, peer_name: str, client_name: str = None, return_addrs: List[addr_type] = None, forward = False, **kwargs):
        super().__init__(**kwargs)
        self.peer_name = peer_name
        self.forward = forward
        if forward:
            assert return_addrs != None
            assert client_name != None
            self.return_addrs = return_addrs
            self.client_name = client_name
        else:
            assert self.name != None
            self.return_addrs = self.addrs
            self.client_name = self.name

    def prepare_payload(self) -> ConnectToPeerRequestPayload:
        return {'peer_name': self.peer_name, 'client_name': self.client_name, 'return_addrs': self.return_addrs}

    def process_response(self, response: Tuple[bool, List[addr_type]]):

        if response == None:
            return None

        if self.forward:
            return response
        
        peer_name = self.peer_name
        client_name = self.client_name
        success, remote_addrs = response
        local_addrs = self.return_addrs

        if not success:
            return None

        self.socket_promise = get_holepunch_socket(local_addrs,remote_addrs)

        tcp_socket = self.socket_promise.wait()

        if tcp_socket == None:
            return None

        pkg_socket = TCPPackageSocket(tcp_socket)
        endpoint = self.context.endpoint.__class__(pkg_socket, self.context.server_context)
        endpoint.register_client(client_name)
        
        return endpoint
