import threading
from typing import Tuple

from protocol.interface import AbstractSerializableRequest

from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext

from .types import addr_type
from .holepunch_util import pipe_port_to_socket

class PortForwardRequest(AbstractSerializableRequest[bool, TCPPackageRequestServerContext]):

    TYPE = 'port_forward'

    def __init__(self, laddr: addr_type, raddr: addr_type, context: TCPPackageRequestServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.laddr = laddr
        self.raddr = raddr

    def prepare_payload(self) -> addr_type:
        return self.raddr

    def process_response(self, response: bool):
        if response == None:
            return False

        successful = response
        if not successful:
            return False

        self.context.endpoint.detach()

        this_sock = self.context.endpoint.socket._tcp_socket

        fwd_thread = threading.Thread(target = pipe_port_to_socket, args = (self.laddr, this_sock))
        fwd_thread.start()

        return True
