import logging
import socketserver
import sys
import threading
import os
import pickle
import logging

from pfl_types.datagram import Msg, RequestType 
from pfl_types.cmd_types import PowerCmd

SOCKET_PATH = '/tmp/power'
logging.basicConfig(level=logging.INFO)


class PowerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        logging.debug('{} received {} from {}'.format(SOCKET_PATH, msg.req_type, self.client_address))
        if msg.req_type == RequestType.RESTART:
            # Kill ourselves and let the watchdog restart us
            raise Exception('Power going down for restart')
        elif msg.req_type == RequestType.PING:
            self.request.sendall(
                pickle.dumps(Msg(RequestType.PING_RESP, None)), 
            )
        elif msg.req_type == RequestType.COMMAND:
            print('Executing command: {}'.format(msg.data))
            if msg.data == PowerCmd.LOW_POWER:
                result = self.is_low_power()
                self.request.sendall(
                    pickle.dumps(Msg(RequestType.DATA, result))
                )

    def is_low_power(self):
        return False

def start_server():
    logging.info('Initializing power server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = socketserver.UnixStreamServer(
        SOCKET_PATH,
        PowerHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
