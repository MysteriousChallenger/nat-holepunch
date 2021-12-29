from protocol.interface import AbstractSerializableRequest

from server.TCPPackageRequestServerContext import TCPPackageRequestServerContext

class GetRegisteredClientsRequest(AbstractSerializableRequest[bool, TCPPackageRequestServerContext]):

    TYPE = 'get_registered_clients'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare_payload(self) -> None:
        return

    def process_response(self, response):
        return response
