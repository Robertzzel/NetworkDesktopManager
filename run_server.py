import time
from Orchestators.server import Server
from configurations import Configurations
import signal, asyncio

ADDRESS = f"{Configurations.CURRENT_IP}:5101"
ADDRESS_INPUT = f"{Configurations.CURRENT_IP}:5102"
ADDRESS_SOUND = f"{Configurations.CURRENT_IP}:5103"


def received_signal(signal, frame):
    print("received signal on server")
    sr.stop()


if __name__ == "__main__":
    sr = Server(ADDRESS, ADDRESS_INPUT, ADDRESS_SOUND)
    signal.signal(signalnum=signal.SIGINT, handler=received_signal)
    asyncio.run(sr.start())

