from typing import List
from protocol.interface import (
    AbstractSerializableHandler,
    RequestData,
)
from server.TCPSocketServerContext import TCPSocketServerContext
from .util import get_registered_clients

class GetRegisteredClientsHandler(AbstractSerializableHandler[TCPSocketServerContext]):

    TYPE = 'get_registered_clients'

    def __init__(self, context: TCPSocketServerContext, **kwargs):
        super().__init__(context=context, **kwargs)
        self.context = context
        self.registered_clients = get_registered_clients(self.context)

    def process_request(self, request: RequestData[None]) -> List[str]:
        return sorted(list(self.registered_clients.keys()))