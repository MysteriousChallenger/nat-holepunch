import socket
import time
import threading
from typing import List, Tuple

from protocol.interface import Promise

from .context_descriptors import RegisteredAddrs, RegisteredName
from .types import addr_type

def accept_holepunch_socket(local_addrs: List[addr_type], timeout: float = 30) -> Promise[socket.socket]:
    socket_promise = Promise[socket.socket]()

    local_priv, local_pub = map(tuple,local_addrs)

    _accept(socket_promise, local_priv) # type: ignore
    _accept(socket_promise, local_pub) # type: ignore

    def timeout_func():
        time.sleep(timeout)
        if not socket_promise.is_set():
            socket_promise.set()

    timeout_timer = threading.Thread(target=timeout_func, daemon=True)
    timeout_timer.start()

    return socket_promise

def connect_holepunch_socket(socket_promise: Promise[socket.socket], local_addrs: List[addr_type], remote_addrs: List[addr_type], timeout: float = 30) -> Promise[socket.socket]:
    local_priv, local_pub = map(tuple,local_addrs)
    remote_priv, remote_pub = map(tuple,remote_addrs)

    _connect(socket_promise, local_priv, remote_priv) # type: ignore
    _connect(socket_promise, local_priv, remote_pub) # type: ignore

    def timeout_func():
        time.sleep(timeout)
        if not socket_promise.is_set():
            socket_promise.set()

    timeout_timer = threading.Thread(target=timeout_func, daemon=True)
    timeout_timer.start()

    return socket_promise


def get_holepunch_socket(local_addrs: List[addr_type], remote_addrs: List[addr_type], timeout: float = 30) -> Promise[socket.socket]:
    socket_promise = Promise[socket.socket]()

    local_priv, local_pub = map(tuple,local_addrs)
    remote_priv, remote_pub = map(tuple,remote_addrs)

    _accept(socket_promise, local_priv) # type: ignore
    _accept(socket_promise, local_pub) # type: ignore 
    _connect(socket_promise, local_priv, remote_priv) # type: ignore
    _connect(socket_promise, local_priv, remote_pub) # type: ignore
    
    def timeout_func():
        time.sleep(timeout)
        if not socket_promise.is_set():
            socket_promise.set()

    timeout_timer = threading.Thread(target=timeout_func, daemon=True)
    timeout_timer.start()

    return socket_promise

def _connect(socket_promise: Promise[socket.socket], local_addr: addr_type, remote_addr: addr_type):
    def connect_job():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind(local_addr)
            s.settimeout(1)

            while not socket_promise.is_set():
                try:
                    s.connect(remote_addr)
                except socket.error:
                    time.sleep(0.1)
                    continue

                if not socket_promise.is_set():
                    socket_promise.set(s)
                return
        except OSError:
            pass

    t = threading.Thread(target=connect_job, daemon=True)
    t.start()

def _accept(socket_promise: Promise[socket.socket], addr: addr_type):
    def accept_job():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind(('', addr[1]))
            s.listen(1)
            s.setblocking(False)

            while not socket_promise.is_set():
                try:
                    conn, _ = s.accept()
                except socket.error:
                    time.sleep(0.1)
                    continue

                if not socket_promise.is_set():
                    socket_promise.set(conn)
                return
        except OSError:
            return

    t = threading.Thread(target=accept_job, daemon=True)
    t.start()
