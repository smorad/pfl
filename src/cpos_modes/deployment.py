#!/usr/bin/env python3

import time
import socket
import pickle
import logging

from cpos_types.datagram import Msg, RequestType
from cpos_servers.fast_socket import FastSocket
from cpos_modes.base_mode import CPOSMode

from cpos_types.cmd_types import CommsCmd

SOCKET_PATH = '/tmp/mode/deployment'
COMMS_SOCKET_PATH = '/tmp/comms'
logging.basicConfig(level=logging.INFO)

class Deployment(CPOSMode):
    def start(self):
        # wait 15 mins
        DEPLOY_WAIT = 1 # will actually be 15 mins
        logging.info('Waiting {} secs to deploy antenna...'.format(DEPLOY_WAIT))
        time.sleep(DEPLOY_WAIT)
        # deploy antenna
        # check IMU for spin decrease
        self.deploy_antenna()
        # update launch status
        # wait 30 mins
        BEACON_WAIT = 1 # this will be 30 mins
        logging.info('Waiting {} secs to begin beacon...'.format(BEACON_WAIT))
        self.beacon()

        # wait for ground signal

    def fail(self):
        '''
        Cleanup in case of failure
        '''
        # retract antenna
        pass

    def deploy_antenna(self) -> bool:
        return Msg(
            RequestType.COMMAND,
            CommsCmd.EXTEND_ANT, 
        ).send_and_recv(SOCKET_PATH, COMMS_SOCKET_PATH, timeout=60 * 5)

    def beacon(self) -> bool:
        return Msg(
            RequestType.COMMAND,
            CommsCmd.SEND_TLM_PKT,
        ).send_and_recv(SOCKET_PATH, COMMS_SOCKET_PATH, timeout=60 * 5)

if __name__ == '__main__':
    Deployment().start()
