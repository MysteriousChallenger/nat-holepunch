from dataclasses import dataclass

from socketIO import TCPPackageSocket

@dataclass
class TCPPackageRequestServerContext():
    endpoint: 'TCPPackageRequestEndpoint' # type: ignore
    endpoint_context: dict
    server_context: dict

