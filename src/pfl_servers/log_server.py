import logging
import socketserver
import sys
import threading
import os
import pickle
import logging

from pfl_servers import base_server
from pfl_types.datagram import Msg, RequestType, LogRequest
from pfl_types.cmd_types import LogCmd

SOCKET_PATH = '/tmp/log'
LOG_DIR = '/tmp/logs'
LOG_PATH = LOG_DIR + '/log'
logging.basicConfig(level=logging.INFO)


class LogHandler(base_server.PFLHandler):

    def __init__(self, *args, **kwargs):
        os.mkdirs(LOG_PATH, exist_ok=True)
        # Rotate on UTC Sundays
        logger = logging.getLogger('rotating_log')
        logger.setLevel(logging.INFO)
        self.logger = logging.TimedRotatingFileHandler(LOG_PATH, when='W6', utc=True)
        super()

    def handle(self):
        # Mebibyte
        msg = pickle.loads(self.request.recv(2 ** 20))
        if self.handle_default(msg):
            return True

        assert(msg.req_type == RequestType.COMMAND_DICT)
        cmd = msg.data['cmd']
        if cmd == LogCmd.ADD_LINES:
            level = msg.data['level']
            source = msg.data[2]
            time = msg.data[3]
            self.logger

    def write(self, lines):
        print('Wrote to log: {}'.format(lines))

def start_server():
    logging.info('Initializing Log server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = base_server.PFLServer(
        SOCKET_PATH,
        LogHandler
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
