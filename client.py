import socket

from server import PackageRequestEndpoint
from socketIO import TCPPackageSocket

HOST, PORT = "127.0.0.1", 59999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

socket = TCPPackageSocket(s)

endpoint = PackageRequestEndpoint(socket)
import time
time.sleep(1)
print("connection terminated")