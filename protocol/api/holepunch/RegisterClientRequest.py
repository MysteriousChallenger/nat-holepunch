from protocol.interface import AbstractSerializableRequest

class RegisterClientRequest(AbstractSerializableRequest[bool]):

    TYPE = 'register_client'

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def prepare_payload(self) -> str:
        return self.name

    def process_response(self, response):
        return response
