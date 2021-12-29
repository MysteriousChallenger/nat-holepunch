from typing import Dict

from protocol.interface import (
    AbstractSerializableHandler,
    RequestData,
)
from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext

from .context_descriptors import ClientAddressDict

class GetRegisteredClientsHandler(AbstractSerializableHandler[TCPPackageRequestServerContext]):

    TYPE = 'get_registered_clients'

    client_address = ClientAddressDict()

    def __init__(self, context: TCPPackageRequestServerContext, **kwargs):
        super().__init__(context=context, **kwargs)

    def process_request(self, request: RequestData[None]) -> Dict:
        return self.client_address