from os import pipe
from typing import Dict, List, Tuple
import threading
import multiprocessing

from protocol.interface import (
    AbstractSerializableHandler,
    RequestData,
)
from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext
from socketIO import TCPPackageSocket

from .types import addr_type
from .holepunch_util import connect_to_addr, pipe_sockets



class PortForwardRequestHandler(AbstractSerializableHandler[TCPPackageRequestServerContext]):

    TYPE = 'port_forward'

    def __init__(self, context: TCPPackageRequestServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.context = context

    def process_request(self, request: RequestData[addr_type]) -> bool:
        this_sock = self.context.endpoint.socket._tcp_socket
        s = connect_to_addr(request.payload)
        pipe_remote_to_client = threading.Thread(target = pipe_sockets, args=(this_sock, s))
        pipe_client_to_remote = threading.Thread(target = pipe_sockets, args=(s, this_sock))
        self.context.endpoint.dispatch_response(request, True)
        self.context.endpoint.detach()
        pipe_remote_to_client.start()
        pipe_client_to_remote.start()
        return True



