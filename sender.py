import time
import threading
from Commons.computer import Computer
from Screen.screen_recorder import Server

ADDRESS = (Computer.get_wifi_ip_address(), 5001)
ADDRESS_MOUSE = (Computer.get_wifi_ip_address(), 5002)


def stop(sr):
    print("STARTING")
    time.sleep(3)
    print("STTTTOP")
    sr.stop()


if __name__ == "__main__":
    sr = Server(ADDRESS, ADDRESS_MOUSE)
    threading.Thread(target=sr.start).start()
    stop(sr)

