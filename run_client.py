from Orchestators.client import Client
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_INPUT = (Configurations.SERVER_IP, 5002)
ADDRESS_SOUND = (Configurations.SERVER_IP, 5003)

if __name__ == "__main__":
    receiver = Client(ADDRESS, ADDRESS_INPUT, ADDRESS_SOUND, "Live")
    try:
        receiver.start()
    except:
        print("stop apelat client")
        receiver.stop()
