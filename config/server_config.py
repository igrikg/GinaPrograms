import socket
import pickle
import os.path as path


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 11111  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            with open(f'{path.dirname(__file__)}/config.conf', 'rb') as f:
               data = f.read(1024)
               while data:
                   data = f.read(1024)
                   if data:
                        break
                   print(data)
                   #conn.sendall(data)