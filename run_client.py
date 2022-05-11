import threading
import time
import sys
from Orchestators.client import Client
from configurations import Configurations
import signal

ADDRESS = (Configurations.SERVER_IP, 5101)
ADDRESS_INPUT = (Configurations.SERVER_IP, 5102)
ADDRESS_SOUND = (Configurations.SERVER_IP, 5103)


def received_signal(sig, frame):
    print("client signal received")
    receiver.stop()


if __name__ == "__main__":
    receiver = Client(ADDRESS, ADDRESS_INPUT, ADDRESS_SOUND)
    signal.signal(signalnum=signal.SIGINT, handler=received_signal)
    receiver.start()


