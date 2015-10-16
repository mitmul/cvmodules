#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import socket
from contextlib import closing


def main():
    host = '10.8.0.141'
    # host = '127.0.0.1'
    # host = '192.168.11.8'
    # host = '192.168.11.23'
    port = 4000
    bufsize = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.connect((host, port))
        sock.send(b'Hello world')
        print(sock.recv(bufsize))
    return
if __name__ == '__main__':
    main()
