#!/usr/bin/env python3

import logging
import time

from pfl_types.datagram import Msg, RequestType
from pfl_types.cmd_types import ADCSCmd, PowerCmd, CommsCmd, StorageCmd
from pfl_servers.fast_socket import FastSocket
from pfl_modes.base_mode import PFLMode

SOCKET_PATH = '/tmp/mode/detumble'
COMMS_SOCKET_PATH = '/tmp/comms'
ADCS_SOCKET_PATH = '/tmp/adcs'
POWER_SOCKET_PATH = '/tmp/power'
STORAGE_SOCKET_PATH = '/tmp/storage'

logging.basicConfig(level=logging.INFO)
class Safe(PFLMode):
    def start(self):
        time.sleep(3)
        low_power = Msg(
            RequestType.COMMAND,
            PowerCmd.LOW_POWER
        ).send_and_recv(SOCKET_PATH, POWER_SOCKET_PATH).data

        try:
            ground_cmd = Msg(
                RequestType.COMMAND,
                CommsCmd.RECV_TLM_PKT
            ).send_and_recv(SOCKET_PATH, COMMS_SOCKET_PATH, timeout=5)
        except:
            # No data from ground
            pass

        if not low_power:

            send_beacon = Msg(
                RequestType.COMMAND,
                CommsCmd.SEND_TLM_PKT
            ).send_and_recv(SOCKET_PATH, COMMS_SOCKET_PATH).data

            # We only want to deploy once
            did_deploy = Msg(
                RequestType.COMMAND,
                [StorageCmd.LOAD, 'DEPLOYED']
            ).send_and_recv(SOCKET_PATH, STORAGE_SOCKET_PATH).data


            if not did_deploy:
                return Deployment

        return Safe


if __name__ == '__main__':
    Safe().start()


from pfl_modes.deployment import Deployment
