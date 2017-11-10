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

from cpos_types.datagram import Msg, RequestType

SERVERS = [cdh_server, comms_server]
SOCK = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
SOCKET_PATH = '/tmp/watchdog'

PING_TIMEOUT = 10

def sock_setup():
    SOCK.setblocking(0)
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    SOCK.bind(SOCKET_PATH)


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

            SOCK.sendto(
                pickle.dumps(Msg(RequestType.PING, None)), 
                server.SOCKET_PATH
            )
            if not select.select([SOCK], [], [], PING_TIMEOUT):
                print('Server {} is not responding to pings, restarting it...')
                proc.terminate()
                proc.join()
                server_procs[server] = boot(server)

        
def main():
    server_procs = {server: boot(server) for server in SERVERS}
    sock_setup()
    watch(server_procs)

if __name__ == '__main__':
    main()
