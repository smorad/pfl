#!/usr/bin/env python3

import time
import socket
import pickle
import logging
import datetime

from pfl_types.datagram import Msg, RequestType
from pfl_servers.fast_socket import FastSocket
from pfl_modes.base_mode import PFLMode
from pfl_modes.detumble import Detumble

from pfl_types.cmd_types import CommsCmd, StorageCmd

SOCKET_PATH = '/tmp/mode/deployment'
COMMS_SOCKET_PATH = '/tmp/comms'
STORAGE_SOCKET_PATH = '/tmp/storage'
logging.basicConfig(level=logging.INFO)

class Deployment(PFLMode):
    def start(self):
        # wait 15 mins
        DEPLOY_WAIT = 1 # will actually be 15 mins
        logging.info('Waiting {} secs to deploy antenna...'.format(DEPLOY_WAIT))
        time.sleep(DEPLOY_WAIT)
        # deploy antenna
        # check IMU for spin decrease
        self.deploy_antenna()
        # update launch status
        uptime, boot_count = self.update_boot_status()
        logging.info('Boot count {}, previous uptime {}'.format(boot_count, uptime))



        # wait 30 mins
        BEACON_WAIT = 1 # this will be 30 mins
        logging.info('Waiting {} secs to begin beacon...'.format(BEACON_WAIT))
        self.beacon()

        # wait for ground signal

        # Write status successful deployment


        Msg(RequestType.COMMAND,
            [StorageCmd.STORE, 'DEPLOYED', 1]
        ).send(SOCKET_PATH, STORAGE_SOCKET_PATH)

        return Detumble

    def update_boot_status(self) -> (float, int):
        '''
        Run on boot. Updates boot count and uptime, and returns
        the current boot count and previous uptime.
        '''
        Msg(RequestType.COMMAND,
            [StorageCmd.STORE, 'LAUNCH', True]
        ).send(SOCKET_PATH, STORAGE_SOCKET_PATH)

        # update boot count
        boot_count = Msg(RequestType.COMMAND,
            [StorageCmd.LOAD, 'BOOT_COUNT']
        ).send_and_recv(SOCKET_PATH, STORAGE_SOCKET_PATH).data
        # The first time this won't be in the DB
        boot_count = boot_count or 0
        boot_count += 1
        Msg(RequestType.COMMAND,
            [StorageCmd.STORE, 'BOOT_COUNT', boot_count]
        ).send(SOCKET_PATH, STORAGE_SOCKET_PATH)

        uptime = Msg(RequestType.COMMAND,
            [StorageCmd.LOAD, 'UPTIME']
        ).send_and_recv(SOCKET_PATH, STORAGE_SOCKET_PATH).data

        Msg(RequestType.COMMAND,
            [StorageCmd.STORE, 'UPTIME', 0]
        ).send(SOCKET_PATH, STORAGE_SOCKET_PATH)

        return uptime, boot_count



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
