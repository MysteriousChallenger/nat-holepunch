from dataclasses import dataclass

from socketIO import TCPPackageSocket

@dataclass
class TCPSocketServerContext():
    socket: TCPPackageSocket
    socket_context: dict
    server_context: dict