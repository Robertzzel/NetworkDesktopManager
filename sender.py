import time
import threading
from Screen.server import Server
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_MOUSE = (Configurations.SERVER_IP, 5002)
ADDRESS_KEYBOARD = (Configurations.SERVER_IP, 5003)


def stop(sr):
    print("STARTING")
    time.sleep(3)
    print("STTTTOP")
    sr.stop()


if __name__ == "__main__":
    sr = Server(ADDRESS, ADDRESS_MOUSE, ADDRESS_KEYBOARD)
    threading.Thread(target=sr.start).start()
    #stop(sr)

