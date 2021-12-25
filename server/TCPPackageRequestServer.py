import socketserver
from .TCPPackageSocketHandler import TCPPackageSocketHandler
from .TCPSocketServer import TCPSocketServer


class TCPPackageRequestServer(TCPSocketServer):
    def __init__(self, server_address, bind_and_activate=True):
        super().__init__(server_address, TCPPackageSocketHandler, bind_and_activate=bind_and_activate)
        self.server_context = dict()

    def finish_request(self, request, client_address) -> None:
        TCPPackageSocketHandler(request, client_address, self, self.server_context)
