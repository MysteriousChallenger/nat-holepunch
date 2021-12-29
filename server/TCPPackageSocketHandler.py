import socketserver

from socketIO import RequestPackage, ResponsePackage, Package, TCPPackageSocket

from .TCPPackageRequestEndpoint import TCPPackageRequestEndpoint
class TCPPackageSocketHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, server_context: dict):
        self.server_context = server_context
        super().__init__(request, client_address, server)

    def setup(self):
        self.request_socket = TCPPackageSocket(_tcp_socket=self.request)

        self.endpoint = TCPPackageRequestEndpoint(self.request_socket, self.server_context)

    def handle(self):
        self.endpoint.wait_until_termination()
        print("connection terminated")

    def finish(self) -> None:
        pass

    @staticmethod
    def is_request(package: Package):
        return isinstance(package, RequestPackage)

    @staticmethod
    def is_response(package: Package):
        return isinstance(package, ResponsePackage)