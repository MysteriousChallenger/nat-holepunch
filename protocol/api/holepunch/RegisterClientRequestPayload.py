from dataclasses import dataclass

from jsonIO import DefaultSerializable

@dataclass
class RegisterClientRequestPayload(DefaultSerializable):
    name: str