import socket, time, math

HOST = "148.6.100.157"
PORT = 12111

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'CLEAR')
    print(s.recv(1024))
    s.sendall(b'START')
    print(s.recv(1024))
    time.sleep(1)
    s.sendall(b'STOP')
    print(s.recv(1024))
    s.sendall(b'BSIZE;8')
    print(s.recv(1024))
    s.sendall(b'DATA')
    data = str(s.recv(1024))[2:-1]
    d_split = str(data).split(';')
    if len(d_split) == 3:
        kbyte = int(d_split[2]) / 1024 / 8
        for i in range(math.ceil(kbyte) + 1):
            s.sendall(b'DATA;OK')
            data1 = s.recv(1024 * 8)
            print(data1)


