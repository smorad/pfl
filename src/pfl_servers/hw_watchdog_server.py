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

TESTING=True

SOCKET_PATH = '/tmp/hardware_watchdog'
logging.basicConfig(level=logging.INFO)

KERNEL_WATCHDOG_DEV = '/dev/pfl_kernel_watchdog'
# TODO: change to be dynamic
PFL_ROOT = '/home/smorad/code/mysat_py/src/'

class HardwareWatchdogHandler(base_server.PFLHandler):
    '''
    This handler exists to ensure that the PFL software watchdog
    is in a functional state. Every time this server receives a ping,
    it will write to the hardware watchdog. If for any reason the PFL
    watchdog stops, this will not send pings to the hw watchdog which
    will trigger a reboot.

    Will also ping the kernel watchdog. This should have a slightly 
    shorter timeout than the HW watchdog, so if PFL dies but the
    kernel is stable, we can do a 'graceful' soft reboot instead
    of a hard power cut.
    '''

    def ping_kernel_watchdog(self) -> None:
        # Stubbed until I get a real linux machine with functional
        # kernel watchdogs
        pass

    def ping_hw_watchdog(self) -> None:
        # Stubbed for now, this should be implemented according to the hardware
        pass

    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        self.handle_default(msg)

        if msg.req_type== RequestType.PING:
            self.ping_kernel_watchdog()
            self.ping_hw_watchdog()

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


def spawn_linux_watchdog():
    '''
    Spawn Linux Kernel watchdog for us to write to as well.
    Make sure you write to it 50 seconds after calling this
    function or you will reboot your system.
    '''
    if not TESTING:
        subprocess.Popen(['watchdog', '-c', PFL_ROOT + 'src/pfl_conf/kernel_watchdog.conf']) 

def start_server():
    logging.info('Initializing HARDWARE_WATCHDOG server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    server = base_server.PFLServer(
        SOCKET_PATH,
        HardwareWatchdogHandler
    )
    
    spawn_linux_watchdog()
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
