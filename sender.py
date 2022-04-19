import time
import threading
from Screen.server import Server
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_INPUT = (Configurations.SERVER_IP, 5002)


def stop(sr):
    print("STARTING")
    time.sleep(3)
    print("STTTTOP")
    sr.stop()


if __name__ == "__main__":
    sr = Server(ADDRESS)
    threading.Thread(target=sr.start).start()
    #stop(sr)

