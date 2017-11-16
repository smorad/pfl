#!/usr/bin/env python3

import logging

from cpos_types.datagram import Msg, RequestType, ADCSCommand
from cpos_servers.fast_socket import FastSocket
from cpos_modes.base_mode import CPOSMode

SOCKET_PATH = '/tmp/mode/detumble'
COMMS_SOCKET_PATH = '/tmp/comms'
ADCS_SOCKET_PATH = '/tmp/adcs'

logging.basicConfig(level=logging.INFO)
class Detumble(CPOSMode):
    def start(self):
        # Check IMU rates
        # if low IMU
            # finish detumble 
        # if power:
            # power on mag coils
            # check receiver
            # if valid ground input
                # finish detumble
        # if timed out:
            # finish detumble
        # check_receiver
            # record telem
            # beacon

        is_tumbling = Msg(
            RequestType.COMMAND, 
            ADCSCommand['IS_TUMBLING']
        ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)

        if not is_tumbling:
            self.finish_detumble()


    def finish_detumble(self):
        '''
        Disable mag coils, record telem, and go to safe mode
        after
        '''
        pass



if __name__:
    Detumble().start()


