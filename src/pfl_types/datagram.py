import enum
import collections
from typing import Any
import pickle
import json

from pfl_servers.fast_socket import FastSocket

RequestType = enum.Enum('RequestType', 
    'POWER_ON POWER_OFF RESTART COMMAND COMMAND_LIST '
    'COMMAND_DICT DATA PING PING_RESP LOG')

PROTO = pickle 

class LogRequest:
    def __init__(self, source, level, time, message):
        self.source = source
        self.level = level
        self.time = time
        self.message = message

class Msg:
    # Can be either json or pickle (pickle is faster, but python specific)
    def __init__(self, req_type: RequestType, data: Any):
        self.req_type = req_type
        self.data = data

    def send(self, src, dest, timeout=None):
        msg = pickle.dumps(self)
        with FastSocket(src, dest, timeout) as sock:
            sock.sendall(msg)

    def send_and_recv(self, src: str, dest: str, timeout: int=None, pkt_size: int=1024):
        '''
        Send a message and wait for a response. RTT could be up to 2 * timeout.
        Returns the response.
        '''
        msg = PROTO.dumps(self)
        with FastSocket(src, dest, timeout) as sock:
            sock.sendall(msg)
            result = sock.recv(pkt_size)
        return PROTO.loads(result)



