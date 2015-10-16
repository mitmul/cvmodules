from __future__ import print_function
import socket
from contextlib import closing


def main():
    # host = '10.8.0.106'
    # host = '127.0.0.1'
    host = '192.168.11.8'
    port = 50007
    backlog = 10
    bufsize = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.bind((host, port))
        sock.listen(backlog)

        while True:
            conn, address = sock.accept()
            with closing(conn):
                msg = conn.recv(bufsize)
                print(msg)
                conn.send(msg)
    return
if __name__ == '__main__':
    main()