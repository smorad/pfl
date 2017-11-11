#!/usr/bin/env python3

import socket
import os

class FastSocket:
    def __init__(self, src, dest, timeout=30):
        self.src = src
        self.dest = dest
        self.timeout = timeout

    def __enter__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(self.src):
            os.unlink(self.src)

        self.sock.bind(self.src)
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.dest)
        return self.sock

    def __exit__(self, *args):
        self.sock.close()

