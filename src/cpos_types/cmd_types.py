# This file enumerates the possible actions for each
# subsystem server. Note that certain commands (POWER_ON, etc)
# are shared between all subsystems, and are implemented in the
# software bus header instead

from enum import Enum

CommsCmd = Enum('CommsCmd',
    ' '.join(
    ['EXTEND_ANT',   # Extend antenna
    'RETRACT_ANT',   # Retract antenna
    'SEND_TLM_PKT',  # Send formatted telemetry packet to ground
    'RECV_TLM_PKT'   # Receive telemetry packet from ground
    ])
)

ADCSCmd = Enum('ADCSCmd',
    ' '.join(
    ['GET_STATE',    # Reply with packet containing pointing angle and position
    'IS_TUMBLING',   # Return whether or not the craft is still tumbling
    'DETUMBLE',      # Detumble spacecraft during deployment phase
    'POINT',         # Point spacecaft at specified angle
    'TRACK'          # Track object
    ])
)

LoggingCmd = Enum('LoggingCmd',
    ' '.join(
    ['GET_LEVEL',    # Return a formatted packet containing all logs at a level
    'GET_LINES',     # Return a formatted packet with N most recent entries
    'GET_TLM'        # Return all unsent logs marked as telemetry
    ])
)

CDHCmd = Enum('CDHCmd',
    ' '.join(
    ['SYNC_CLOCKS',  # Send out a heartbeat to sync all subsystem clocks
    'EXEC_CMD'       # For emergencies: run a shell command
    ])
)
