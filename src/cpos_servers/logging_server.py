import logging
import socketserver
import os
import pickle

from cpos_types.datagram import Msg, RequestType 
#
#SOCKET_PATH = '/tmp/log'
#
#class LoggingHandler(socketserver.BaseRequestHandler):
#    def handle(self):
#        msg = pickle.loads(self.request.recv(1024))
#        print('{} received {} from {}'.format(SOCKET_PATH, msg.req_type, self.client_address))
#        if msg.req_type == RequestType.RESTART:
#            # Kill ourselves and let the watchdog restart us
#            raise Exception('CDH going down for restart')
#        elif msg.req_type == RequestType.PING:
#            self.request.sendall(
#                pickle.dumps(Msg(RequestType.PING_RESP, None)), 
#            )
#        elif msg.req_type == RequestType.LOG:
#            time, level, module, message = msg.data
#            self.log('{} - {} - {} - {}'.format(time, level, module, message))
#
#    def setup(self):
#        super()
#        FORMAT = '(message)s'
#        self.log = logging.getLogger('root')
#        self.log.setLevel(logging.INFO)
#        console = logging.StreamHandler()
#        console.setLevel(logging.INFO)
#        formatter = logging.Formatter(FORMAT)
#        console.setFormatter(formatter)
#        
#        self.log.addHandler(console)
#
#def start_server():
#    #self.logger.info('Initializing LOG server...')
#    if os.path.exists(SOCKET_PATH):
#        print('Detected stale socket, removing to start server...')
#        os.remove(SOCKET_PATH)
#
#    server = socketserver.UnixStreamServer(
#        SOCKET_PATH,
#        LoggingHandler 
#    )
#    try:
#        server.serve_forever()
#    finally:
#        # Make sure to remove socket if handler crashes
#        os.remove(SOCKET_PATH)
#
#if __name__ == '__main__':
#    start_server()

def setup():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    log.addHandler(console)
    return log
