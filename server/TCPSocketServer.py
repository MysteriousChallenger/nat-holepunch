import socketserver

class TCPSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    request_queue_size = 1024
    allow_reuse_address = True
