import time
import threading
from Orchestators.server import Server
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_INPUT = (Configurations.SERVER_IP, 5002)
ADDRESS_SOUND = (Configurations.SERVER_IP, 5003)


def stop(sr):
    print("STARTING")
    time.sleep(3)
    print("STTTTOP")
    sr.stop()


if __name__ == "__main__":
    sr = Server(ADDRESS, ADDRESS_INPUT, ADDRESS_SOUND)
    try:
        sr.start()
    except:
        print("stop apelat server")
        sr.stop()

