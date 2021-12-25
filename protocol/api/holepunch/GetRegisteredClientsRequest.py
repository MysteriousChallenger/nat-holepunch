from protocol.interface import AbstractSerializableRequest

class GetRegisteredClientsRequest(AbstractSerializableRequest[bool]):

    TYPE = 'get_registered_clients'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare_payload(self) -> None:
        return

    def process_response(self, response):
        print(response)
        return response
