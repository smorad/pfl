#!/usr/bin/env python3

import logging
import socketserver
import sys
import threading
import os
import pickle
import time
import logging

from pfl_servers import base_server
from pfl_types.datagram import Msg, RequestType 
from pfl_types.cmd_types import CommsCmd

SOCKET_PATH = '/tmp/comms'
logging.basicConfig(level=logging.INFO)

class CommsHandler(base_server.PFLHandler):
    def deploy_antenna(self) -> bool:
        time.sleep(1)
        return True

    def beacon(self) -> bool:
        time.sleep(1)
        return True

    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        if self.handle_default(msg):
            return

        if msg.data == CommsCmd.EXTEND_ANT:
            result = self.deploy_antenna()
            logging.info('antenna deployment result: {}'.format(result))
            self.request.sendall(
                pickle.dumps(Msg(RequestType.DATA, result)), 
            )
        elif msg.data == CommsCmd.SEND_TLM_PKT:
            result = self.beacon()
            logging.info('Beacon result: {}'.format(result))
            self.request.sendall(
                pickle.dumps(Msg(RequestType.DATA, result))
            )


def start_server():
    logging.info('Initializing COMMS server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = base_server.PFLServer(
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
