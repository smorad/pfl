import enum
import collections
from typing import Any

RequestType = enum.Enum('RequestType', 
    'POWER_ON POWER_OFF RESTART COMMAND DATA PING PING_RESP')

CommsCommandAction = enum.Enum('CommsCommandAction',
    'EXTEND_ANT RETRACT_ANT')

class Msg:
    def __init__(self, req_type: RequestType, data: Any):
        self.req_type = req_type
        # TODO: python bug where self.client_address is not populated,
        # put it in the packet instead
        self.data = data


