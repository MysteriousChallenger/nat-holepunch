import socketserver
import time

import jsonIO
from server import TCPPackageSocketHandler, TCPSocketServer

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 59999

    # Create the server, binding to localhost on port 9999
    with TCPSocketServer((HOST, PORT), TCPPackageSocketHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
