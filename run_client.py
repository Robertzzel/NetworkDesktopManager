import threading
import time
import sys
from Orchestators.client import Client
from configurations import Configurations
import signal, asyncio

ADDRESS = f"{Configurations.SERVER_IP}:5101"
ADDRESS_INPUT = f"{Configurations.SERVER_IP}:5102"
ADDRESS_SOUND = f"{Configurations.SERVER_IP}:5103"


def received_signal(sig, frame):
    print("client signal received")
    receiver.stop()


if __name__ == "__main__":
    receiver = Client(ADDRESS, ADDRESS_INPUT, ADDRESS_SOUND)
    signal.signal(signalnum=signal.SIGINT, handler=received_signal)
    asyncio.run(receiver.start())


