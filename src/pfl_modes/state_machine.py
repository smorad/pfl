#!/usr/bin/env python3

from pfl_modes.safe_mode import Safe
from pfl_servers import storage_server
import logging

TESTING = True

class StateMachine:
    # Start in safe mode
    # After timer switch to deployment mode
    # After deployment switch to comms if successful, retry mode if failed
    
    state = Safe

    def __init__(self):
        if TESTING:
            clean_db()
        while(True):
            logging.info('Transition to state: {}'.format(self.state))
            self.state = self.state().start()


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


if __name__ == '__main__':
    StateMachine()
