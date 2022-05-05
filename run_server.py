import time
import threading
from Orchestators.server import Server
from configurations import Configurations
import signal

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_INPUT = (Configurations.SERVER_IP, 5002)
ADDRESS_SOUND = (Configurations.SERVER_IP, 5003)


def received_signal(signal, frame):
    print("received signal on server")
    sr.stop()
    time.sleep(1)
    exit(0)


if __name__ == "__main__":
    sr = Server(ADDRESS, ADDRESS_INPUT, ADDRESS_SOUND)
    signal.signal(signalnum=signal.SIGINT, handler=received_signal)
    sr.start()


