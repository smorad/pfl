#!/usr/bin/env python3

import multiprocessing
import time
from typing import Any, Tuple, List, Dict
import socket
import select
import pickle
import os
import logging

import cpos_servers.logging_server
from cpos_servers import cdh_server
from cpos_servers import comms_server
from cpos_types.datagram import Msg, RequestType
from cpos_servers.fast_socket import FastSocket


from cpos_types.datagram import Msg, RequestType

SERVERS = [cdh_server, comms_server]

SOCKET_PATH = '/tmp/watchdog'
logging.basicConfig(level=logging.INFO)

def boot(server):
    proc = multiprocessing.Process(target=server.start_server)
    proc.start()
    return proc

        
def watch(server_procs: Dict[Any, multiprocessing.Process]):
    '''
    Ensure servers are running, and are responding to pings
    '''
    logging.info('Watchdog started')
    while(True):
        time.sleep(5)
        for server, proc in server_procs.items():
            if not proc.is_alive():
                logging.error('Server {} is not alive, restarting it...'.format(server))
                server_procs[server] = boot(server)

            with FastSocket(SOCKET_PATH, server.SOCKET_PATH, timeout=120) as sock:
                sock.sendall(pickle.dumps(Msg(RequestType.PING, None))) 

                try:
                    sock.recv(1024)
                except OSError:
                    logging.error('Server {} is not responding to pings, restarting it...')
                    proc.terminate()
                    proc.join()
                    server_procs[server] = boot(server)

        
def main():
    server_procs = {server: boot(server) for server in SERVERS}
    watch(server_procs)

if __name__ == '__main__':
    main()
