import logging
import socketserver
import sys
import threading
import os
import pickle

from cpos_types.datagram import Msg, RequestType 

SOCKET_PATH = '/tmp/cdh'

class CDHHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        print('{} received {} from {}'.format(SOCKET_PATH, msg.req_type, self.client_address))
        if msg.req_type == RequestType.RESTART:
            # Kill ourselves and let the watchdog restart us
            raise Exception('CDH going down for restart')
        elif msg.req_type == RequestType.PING:
            self.request.sendall(
                pickle.dumps(Msg(RequestType.PING_RESP, None)), 
            )
        elif msg.req_type == RequestType.COMMAND:
            print('Executing command: {}'.format(msg.data))

def start_server():
    print('Initializing CDH server...')
    if os.path.exists(SOCKET_PATH):
        print('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = socketserver.UnixStreamServer(
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
