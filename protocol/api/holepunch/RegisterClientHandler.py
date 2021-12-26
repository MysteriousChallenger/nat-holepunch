from protocol.interface import (
    AbstractSerializableHandler,
    RequestData,
)
from server.TCPSocketServerContext import TCPSocketServerContext

from .util import get_registered_clients
from .RegisterClientRequestPayload import RegisterClientRequestPayload
class RegisterClientHandler(AbstractSerializableHandler[TCPSocketServerContext]):

    TYPE = 'register_client'

    def __init__(self, context: TCPSocketServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.context = context
        self.registered_clients = get_registered_clients(self.context)
        self.name = None

    def process_request(self, request: RequestData[RegisterClientRequestPayload]) -> bool:
        name = request.payload['name']

        if name in self.registered_clients:
            return False

        if self.name != None:
            del self.registered_clients[self.name]

        self.name = name
        socket = self.context.socket
        print(socket._tcp_socket.getpeername())
        print(request.payload['addr'])
        self.registered_clients[name] = socket
        return True

    def __del__(self):
        if self.name != None:
            del self.registered_clients[self.name]