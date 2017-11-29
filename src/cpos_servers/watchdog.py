#!/usr/bin/env python3

import multiprocessing
import time
from typing import Any, Tuple, List, Dict
import socket
import select
import pickle
import os
import logging
import hashlib

from cpos_servers import cdh_server
from cpos_servers import comms_server
from cpos_servers import adcs_server
from cpos_servers import power_server
from cpos_servers import log_server
from cpos_servers import storage_server

from cpos_types.datagram import Msg, RequestType
from cpos_servers.fast_socket import FastSocket


from cpos_types.datagram import Msg, RequestType

SERVERS = [cdh_server, comms_server, adcs_server, power_server, storage_server]

SOCKET_PATH = '/tmp/watchdog'
logging.basicConfig(level=logging.INFO)

def boot(server):
    proc = multiprocessing.Process(target=server.start_server)
    proc.start()
    return proc

def checksum(server):
    with open(server.__file__, 'rb') as f:
        sha1_sum = hashlib.sha1(f.read()).hexdigest()
    sum_file = server.__file__ + '.checksum'
    
    # TODO: remove me once files stop changing
    if not os.path.isfile(sum_file):
        with open(sum_file, 'w+') as f:
            f.write(str(sha1_sum))

    with open(sum_file, 'r') as f:
        cached_sum = f.read()
        if sha1_sum != cached_sum:
            logging.critical('Server {} checksum mismatch: {} {}'.format(server, cached_sum, sha1_sum))

        
def server_ping(server):
    with FastSocket(SOCKET_PATH, server.SOCKET_PATH, timeout=60) as sock:
        sock.sendall(pickle.dumps(Msg(RequestType.PING, None))) 

        try:
            sock.recv(1024)
            return True
        except OSError:
            return False

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

            if not server_ping(server):
                logging.error('Server {} is not responding to pings, restarting it...'.format(server))
                proc.terminate()
                proc.join()
                server_procs[server] = boot(server)

            # TODO renable checksum when files stop changing
            #checksum(server)

        
def main():
    server_procs = {server: boot(server) for server in SERVERS}
    watch(server_procs)

if __name__ == '__main__':
    main()
