import socketserver
import time

import jsonIO
from server import TCPPackageRequestServer

if __name__ == "__main__":
    HOST, PORT = "", 59998

    # Create the server, binding to localhost on port 9999
    with TCPPackageRequestServer((HOST, PORT)) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
