import socketserver

from server.PackageRequestEndpoint import PackageRequestEndpoint
from socketIO import RequestPackage, ResponsePackage, TCPPackageSocket
from socketIO.interface import Package


class TCPPackageSocketHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.request_socket = TCPPackageSocket(_tcp_socket=self.request)

        self.endpoint = PackageRequestEndpoint(self.request_socket)

    def handle(self):
        print(self.endpoint.PING())
        import time
        self.endpoint.wait_until_termination()
        print("connection terminated")

    @staticmethod
    def is_request(package: Package):
        return isinstance(package, RequestPackage)

    @staticmethod
    def is_response(package: Package):
        return isinstance(package, ResponsePackage)
