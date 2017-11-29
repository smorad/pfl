#!/usr/bin/env python3

from pfl_modes.safe_mode import Safe
import logging

class StateMachine:
    # Start in safe mode
    # After timer switch to deployment mode
    # After deployment switch to comms if successful, retry mode if failed
    
    state = Safe

    def __init__(self):
        while(True):
            logging.info('Transition to state: {}'.format(self.state))
            state = self.state().start()



if __name__ == '__main__':
    StateMachine()
