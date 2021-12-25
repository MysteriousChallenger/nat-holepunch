import socket
from threading import Thread
import time

from server import TCPPackageRequestEndpoint, TCPPackageSocketHandler
from socketIO import TCPPackageSocket

HOST, PORT = "127.0.0.1", 59999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
endpoint.get_registered_clients()
input()
print("connection terminated")