import socketserver

class TCPSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    request_queue_size = 1024
