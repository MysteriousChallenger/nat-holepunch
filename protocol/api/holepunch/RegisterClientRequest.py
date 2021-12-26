from protocol.interface import AbstractSerializableRequest

from server.TCPSocketServerContext import TCPSocketServerContext

from .RegisterClientRequestPayload import RegisterClientRequestPayload
class RegisterClientRequest(AbstractSerializableRequest[bool, TCPSocketServerContext]):

    TYPE = 'register_client'

    def __init__(self, name: str, context: TCPSocketServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.context=context
        self.name = name

    def prepare_payload(self) -> RegisterClientRequestPayload:
        return {'name': self.name, 'addr': self.context.socket._tcp_socket.getsockname()}

    def process_response(self, response):
        return response
