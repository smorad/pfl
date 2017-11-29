import logging
import socketserver
import sys
import threading
import os
import pickle
import logging
import shelve

from cpos_servers import base_server
from cpos_types.datagram import Msg, RequestType 
from cpos_types.cmd_types import StorageCmd

SOCKET_PATH = '/tmp/storage'
DB_PATH = '/tmp/persist-storage'
MAX_FILE_SIZE = 2 ** 27     # 128 Mebibytes

logging.basicConfig(level=logging.INFO)

#TODO: Add some robustness on server reload in case db file gets corrupted
class StorageHandler(base_server.CPOSHandler):
    def handle(self):
        msg = pickle.loads(self.request.recv(MAX_FILE_SIZE))
        if self.handle_default(msg):
            return True

        if msg.data[0] == StorageCmd.STORE:
            with shelve.open(DB_PATH, 'c') as db:
                # Make sure we don't have None as saved data,
                # we should explicitly write zero instead
                assert(msg.data[1] and msg.data[2] != None)
                db[msg.data[1]] = msg.data[2]

        elif msg.data[0] == StorageCmd.LOAD:
            with shelve.open(DB_PATH, 'r') as db:
                try:
                    msg = db[msg.data[1]]
                except KeyError:
                    logging.warn('No entry {} in storage'.format(msg.data[1]))
                    msg = None
                self.request.sendall(
                    pickle.dumps(Msg(RequestType.DATA, msg))
                )
                

def start_server():
    logging.info('Initializing storage server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = base_server.CPOSServer(
        SOCKET_PATH,
        StorageHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
