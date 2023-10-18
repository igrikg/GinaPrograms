# echo-client.py

import socket
import pickle


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 11111  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"get_config")
    data = s.recv(1024)
print(f"Received {data}")


class Configuration(dict):
    def __init__(self):
        super().__init__(self)
        with open(f'{path.dirname(__file__)}/config.conf', 'rb') as f:
            self.update()
