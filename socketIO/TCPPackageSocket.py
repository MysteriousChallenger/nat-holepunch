from socket import socket
from typing import Callable, Generic, TypeVar

import jsonIO
from socketIO import GeneralPurposeSocket, PackageSocketShutdownException

from .interface import DuplicableSocket, Package

PackageType = TypeVar("PackageType", bound=Package)


class TCPPackageSocket(GeneralPurposeSocket, Generic[PackageType]):
    def __init__(
        self,
        _tcp_socket: socket,
        _timeout=10,
        _shutdown_callback: Callable[[], None] = None,
        _underlying: DuplicableSocket = None,
        filter: Callable[[Package], bool] = lambda _: True,
        **kwargs
    ):
        super().__init__(
            _underlying=_underlying,
            filter=filter,
            _shutdown_callback=_shutdown_callback,
            **kwargs
        )
        self._tcp_socket = _tcp_socket
        self._timeout = _timeout

        self._tcp_socket.settimeout(_timeout)
        self._socket_buf = b""

    def send(self, package: Package):
        package_bytes = jsonIO.dumps(package).encode()
        # print()
        # print("send:")
        # print(package_bytes.decode())
        size = len(package_bytes).to_bytes(4, byteorder="little")
        self.socket_send(size)
        self.socket_send(package_bytes)

    def recv(self) -> PackageType:
        msg_size = int.from_bytes(self.socket_recv(4), byteorder="little")
        data = self.socket_recv(msg_size)
        # print()
        # print("recv:")
        # print(data.decode())
        return jsonIO.loads(data.decode())

    def socket_recv(self, n_bytes) -> bytes:
        try:
            if self.is_open == False:
                raise OSError
            bytes = self._socket_buf
            while len(bytes) < n_bytes:
                recv_bytes = self._tcp_socket.recv(n_bytes - len(bytes))
                if len(recv_bytes) == 0:
                    raise OSError
                bytes += recv_bytes

            bytes = bytes[:n_bytes]
            self._socket_buf = bytes[n_bytes:]

            return bytes
        except OSError:
            self.close()
            raise PackageSocketShutdownException

    def socket_send(self, bytes) -> None:
        try:
            if self.is_open == False:
                raise OSError
            self._tcp_socket.sendall(bytes)
        except OSError:
            self.close()
            raise PackageSocketShutdownException

    def close(self):
        self._tcp_socket.close()
        super().close()
