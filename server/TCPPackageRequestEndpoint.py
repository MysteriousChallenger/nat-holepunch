from socketIO import TCPPackageSocket

from .TCPSocketServerContext import TCPSocketServerContext
from .PackageRequestEndpoint import PackageRequestEndpoint

class TCPPackageRequestEndpoint(PackageRequestEndpoint[TCPSocketServerContext]):
    def __init__(self, socket: TCPPackageSocket, server_context: dict, **kwargs):
        self.socket = socket 
        self.socket_context = dict()
        self.server_context = server_context
        super().__init__(socket = socket, **kwargs)

    def get_context(self) -> TCPSocketServerContext:
        return TCPSocketServerContext(
            socket=self.socket, 
            socket_context=self.socket_context, 
            server_context=self.server_context)
        
