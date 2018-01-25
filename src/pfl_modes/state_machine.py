#!/usr/bin/env python3

import os
import pickle

from pfl_modes.safe_mode import Safe
from pfl_servers import storage_server, base_server
from pfl_types.datagram import Msg, RequestType 
import logging

TESTING = True

SOCKET_PATH = '/tmp/state_machine'
logging.basicConfig(level=logging.INFO)


class StateMachineHandler(base_server.PFLHandler):
    '''
    Different than the other servers. The state machine is 
    the "driver" that drives the other servers. The state machine
    will only switch phases upong receiving a PING request from the
    watchdog. This ensures the state machine doesn't keep running
    if we end up in a bad state.

    This also means that we can only move one phase every ping delay.
    '''
    
    state = Safe


    def handle(self):
        msg = pickle.loads(self.request.recv(1024))
        self.handle_default(msg)
        if msg.req_type == RequestType.PING:
            # Wait for ping from watchdog to execute phases
            self.state = self.state().start()
            logging.info('Transitioning to state {}'.format(self.state))

def clean_db():
    '''
    Flush the DB to default to simulate a first run
    '''
    import os 
    import shelve
    try:
        os.unlink(storage_server.DB_PATH)
    except OSError:
        pass

    with shelve.open(storage_server.DB_PATH, 'c'):
        pass


def start_server():
    logging.info('Initializing State Machine server...')
    if os.path.exists(SOCKET_PATH):
        logging.warn('Detected stale socket, removing to start server...')
        os.remove(SOCKET_PATH)

    if TESTING:
        clean_db()

    server = base_server.PFLServer(
        SOCKET_PATH,
        StateMachineHandler    
    )
    try:
        server.serve_forever()
    finally:
        # Make sure to remove socket if handler crashes
        os.remove(SOCKET_PATH)

if __name__ == '__main__':
    start_server()
