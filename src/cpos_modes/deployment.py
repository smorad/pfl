#!/usr/bin/env python3

import time
import socket
import pickle
import logging

from cpos_types.datagram import Msg, RequestType
from cpos_servers.fast_socket import FastSocket
from cpos_modes.base_mode import CPOSMode

SOCKET_PATH = '/tmp/mode/deployment'
COMMS_SOCKET_PATH = '/tmp/comms'
logging.basicConfig(level=logging.INFO)

class Deployment(CPOSMode):
    def start(self):
        # wait 15 mins
        DEPLOY_WAIT = 3 # will actually be 15 mins
        logging.info('Waiting {} secs to deploy antenna...'.format(DEPLOY_WAIT))
        time.sleep(DEPLOY_WAIT)
        # deploy antenna
        # send command
        self.deploy_antenna()
        # update launch status
        # cdh
        # wait 30 mins

        # beacon

        # wait for signal

        # detumble

    def deploy_antenna(self) -> bool:
        msg = pickle.dumps(Msg(
            RequestType.COMMAND,
            'deploy antenna',
        ))

        with FastSocket(SOCKET_PATH, COMMS_SOCKET_PATH, timeout=60 * 5) as sock:
            sock.sendall(msg)
            resp = sock.recv(1024)
        return pickle.loads(resp)

if __name__ == '__main__':
    Deployment().start()
