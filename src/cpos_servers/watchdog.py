from cpos_types.datagram import Msg, RequestType
import multiprocessing

import cdh_server
import comms_server
import time
from typing import Any, Tuple, List, Dict
import socket
import select

import pickle
import json
import os
from fast_socket import FastSocket

from cpos_types.datagram import Msg, RequestType

SERVERS = [cdh_server, comms_server]

SOCKET_PATH = '/tmp/watchdog'

def boot(server):
    proc = multiprocessing.Process(target=server.start_server)
    proc.start()
    return proc

        
def watch(server_procs: Dict[Any, multiprocessing.Process]):
    '''
    Ensure servers are running, and are responding to pings
    '''
    while(True):
        time.sleep(1)
        for server, proc in server_procs.items():
            if not proc.is_alive():
                print('Server {} is not alive, restarting it...'.format(server))
                server_procs[server] = boot(server)

            with FastSocket(SOCKET_PATH, server.SOCKET_PATH, timeout=120) as sock:
                sock.sendall(pickle.dumps(Msg(RequestType.PING, None))) 

                try:
                    sock.recv(1024)
                except OSError:
                    print('Server {} is not responding to pings, restarting it...')
                    proc.terminate()
                    proc.join()
                    server_procs[server] = boot(server)

        
def main():
    server_procs = {server: boot(server) for server in SERVERS}
    watch(server_procs)

if __name__ == '__main__':
    main()
