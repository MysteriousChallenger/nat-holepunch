from socketIO import TCPPackageSocket
from weakref import proxy

from .TCPPackageRequestServerContext import TCPPackageRequestServerContext
from .PackageRequestEndpoint import PackageRequestEndpoint

class TCPPackageRequestEndpoint(PackageRequestEndpoint[TCPPackageRequestServerContext]):
    def __init__(self, socket: TCPPackageSocket, server_context: dict, **kwargs):
        self.socket = socket 
        self.endpoint_context = dict()
        self.server_context = server_context
        super().__init__(socket = socket, **kwargs)

    def get_context(self) -> TCPPackageRequestServerContext:
        return TCPPackageRequestServerContext(
            endpoint=proxy(self), 
            endpoint_context=self.endpoint_context, 
            server_context=self.server_context)
        
