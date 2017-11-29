#!/usr/bin/env python3

import logging

from pfl_types.datagram import Msg, RequestType
from pfl_types.cmd_types import ADCSCmd, PowerCmd
from pfl_servers.fast_socket import FastSocket
from pfl_modes.base_mode import PFLMode

SOCKET_PATH = '/tmp/mode/detumble'
COMMS_SOCKET_PATH = '/tmp/comms'
ADCS_SOCKET_PATH = '/tmp/adcs'
POWER_SOCKET_PATH = '/tmp/power'

logging.basicConfig(level=logging.INFO)
class Safe(PFLMode):
    def start(self):
        low_power = Msg(
            RequestType.COMMAND,
            PowerCmd.LOW_POWER
        ).send_and_recv(SOCKET_PATH, POWER_SOCKET_PATH)

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
            ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)


if __name__ == '__main__':
    Safe().start()


