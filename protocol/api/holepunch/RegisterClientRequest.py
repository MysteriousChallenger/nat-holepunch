from protocol.interface import AbstractSerializableRequest

from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext

from .types import RegisterClientRequestPayload
from .context_descriptors import RegisteredName, RegisteredAddrs
class RegisterClientRequest(AbstractSerializableRequest[bool, TCPPackageRequestServerContext]):

    TYPE = 'register_client'

    name = RegisteredName()
    addrs = RegisteredAddrs()

    def __init__(self, name: str, context: TCPPackageRequestServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.proposed_name = name

    def prepare_payload(self) -> RegisterClientRequestPayload:
        return {'name': self.proposed_name, 'addr': self.context.endpoint.socket._tcp_socket.getsockname()} # type: ignore

    def process_response(self, response):
        if response == None:
            return False

        successful, addrs = response
        if not successful:
            return False

        self.name = self.proposed_name
        self.addrs = addrs
        
        return True
