import socket
from threading import Thread
import time

from server import TCPPackageRequestEndpoint, TCPPackageSocketHandler
from socketIO import TCPPackageSocket

HOST, PORT = "127.0.0.1", 59998

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

s.connect((HOST, PORT))

socket = TCPPackageSocket(s)

print('start')

endpoint = TCPPackageRequestEndpoint(socket,dict())
print('start')
def keep_alive():
    while True:
        endpoint.ping()
        time.sleep(4)

keep_alive_thread = Thread(target=keep_alive, daemon=True)
keep_alive_thread.start()
print('start')

name = input("name: ")
endpoint.register_client(name)
input()
print(endpoint.get_registered_clients())
input()
name = input("name: ")
e2 = (endpoint.connect_to_peer(name))
print(e2.ping())
print(e2.get_registered_clients())
print("connection terminated")