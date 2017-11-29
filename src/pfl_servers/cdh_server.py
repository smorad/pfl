import logging
import socketserver
import sys
import threading
import os
import pickle
import logging

from pfl_servers import base_server
from pfl_types.datagram import Msg, RequestType 

SOCKET_PATH = '/tmp/cdh'
logging.basicConfig(level=logging.INFO)


class CDHHandler(base_server.PFLHandler):
    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        if self.handle_default(msg):
            return True

def start_server():
    logging.info('Initializing CDH server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = base_server.PFLServer(
        SOCKET_PATH,
        CDHHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
