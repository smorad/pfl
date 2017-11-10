import time
import socket

SOCKET_PATH = '/tmp/mode/deployment'
COMMS_SOCKET_PATH = '/tmp/comms'

class Deployment(CPOSMode):
    def start(self):
        self.init_socket()
        # wait 15 mins
        time.sleep(15 * 60)
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
        return True

    def init_socket(self) -> socket.socket:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(SOCKET_PATH)
        self.sock.settimeout(60)
