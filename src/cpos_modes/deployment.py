import time
import socket
import pickle


from cpos_types.datagram import Msg, RequestType
from cpos_servers.fast_socket import FastSocket
# TODO: remove after testing
#from cpos_servers import watchdog
from base_mode import CPOSMode

# TODO: remove after testing
#watchdog.main()
SOCKET_PATH = '/tmp/mode/deployment'
COMMS_SOCKET_PATH = '/tmp/comms'

class Deployment(CPOSMode):
    def start(self):
        # wait 15 mins
        DEPLOY_WAIT = 3 # will actually be 15 mins
        print('Waiting {} secs to deploy antenna...'.format(DEPLOY_WAIT))
        time.sleep(DEPLOY_WAIT)
        # deploy antenna
        # send command
        self.deploy_antenna()
        # update launch status
        # cdh
        # wait 30 mins

        # beacon

        # wait for signal

        # detumble

    def deploy_antenna(self) -> bool:
        msg = pickle.dumps(Msg(
            RequestType.COMMAND,
            'deploy antenna',
        ))

        with FastSocket(SOCKET_PATH, COMMS_SOCKET_PATH, timeout=60 * 5) as sock:
            sock.sendall(msg)
            resp = sock.recv(1024)
            print(resp)
        return pickle.loads(resp)
