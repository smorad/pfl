import logging
import socketserver
import sys
import threading
import os
import pickle
import logging

from pfl_types.datagram import Msg, RequestType
from pfl_types.cmd_types import ADCSCmd
from pfl_servers.fast_socket import FastSocket
from pfl_servers import base_server

SOCKET_PATH = '/tmp/adcs'
logging.basicConfig(level=logging.INFO)


class ADCSHandler(base_server.PFLHandler):
    def handle(self):
        try:
            msg = pickle.loads(self.request.recv(1024))
            if self.handle_default(msg):
                return
            if msg.data == ADCSCmd.IS_TUMBLING:
                result = self.is_tumbling()
                self.request.sendall(
                    pickle.dumps(Msg(RequestType.DATA, result))
                )
            elif msg.data == ADCSCmd.DETUMBLE:
                result = self.detumble()
                self.request.sendall(
                    pickle.dumps(Msg(RequestType.DATA, result))
                )
            else:
                logging.error('Msg {} could not be executed'.format(self.msg))
        except Exception as e:
            print(e)


    def is_tumbling(self):
        return False

    def detumble(self):
        # Power on coils, spinup reaction wheels for a time
        # power off coils, return
        time.sleep(2)
        return True

def start_server():
    logging.info('Initializing ADCS server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = base_server.PFLServer(
        SOCKET_PATH,
        ADCSHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
