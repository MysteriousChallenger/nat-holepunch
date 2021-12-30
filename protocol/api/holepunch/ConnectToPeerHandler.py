from typing import Dict, List, Tuple
import threading

from protocol.interface import (
    AbstractSerializableHandler,
    RequestData,
)
from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext
from socketIO import TCPPackageSocket

from .context_descriptors import ClientAddressDict, ClientDict, ClientName, RegisteredAddrs, RegisteredName
from .types import ConnectToPeerRequestPayload, addr_type
from .holepunch_util import get_holepunch_socket


class ConnectToPeerHandler(AbstractSerializableHandler[TCPPackageRequestServerContext]):

    TYPE = 'connect_to_peer'

    client_address = ClientAddressDict()
    clients = ClientDict()
    name = RegisteredName()
    addrs = RegisteredAddrs()

    def __init__(self, context: TCPPackageRequestServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.context = context

    def process_request(self, request: RequestData[ConnectToPeerRequestPayload]) -> Tuple[bool, List[addr_type]]:
        peer_name = request.payload['peer_name']
        client_name = request.payload['client_name']
        remote_addrs = request.payload['return_addrs']
        local_addrs = self.addrs

        if peer_name == self.name:

            def register_peer():
                socket_promise = get_holepunch_socket(local_addrs,remote_addrs)
                tcp_socket = socket_promise.wait()
                
                if tcp_socket == None:
                    return

                pkg_socket = TCPPackageSocket(tcp_socket)
                endpoint = self.context.endpoint.__class__(pkg_socket, self.context.server_context)
                endpoint.register_client(peer_name)

            t = threading.Thread(target=register_peer, daemon=True)
            t.start()

            return True, self.addrs
        
        if peer_name in self.clients:
            return getattr(self.clients[peer_name], self.TYPE)(peer_name, client_name, remote_addrs, forward = True)

        return False, []    

