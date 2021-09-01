import socketserver


class TCPSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    request_queue_size = 1024

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.socket.setblocking(True)
