#!/usr/bin/env python3

import logging
import socketserver
import sys
import threading
import os
import pickle
import time
import logging

from cpos_types.datagram import Msg, RequestType 

SOCKET_PATH = '/tmp/comms'
logging.basicConfig(level=logging.INFO)

class CommsHandler(socketserver.BaseRequestHandler):
    def deploy_antenna(self) -> bool:
        time.sleep(10)
        return True

    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        logging.debug('{} received {} from {}'.format(SOCKET_PATH, msg.req_type, self.client_address))
        if msg.req_type == RequestType.PING:
            self.request.sendall(
                pickle.dumps(Msg(RequestType.PING_RESP, None)), 
            )
        elif msg.req_type == RequestType.COMMAND:
            logging.info('Executing command: {}'.format(msg.data))
            if msg.data == 'deploy antenna':
                result = self.deploy_antenna()
                logging.info('antenna deployment result: {}'.format(result))
                self.request.sendall(
                    pickle.dumps(Msg(RequestType.DATA, result)), 
                )


def start_server():
    logging.info('Initializing COMMS server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = socketserver.UnixStreamServer(
        SOCKET_PATH,
        CommsHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
