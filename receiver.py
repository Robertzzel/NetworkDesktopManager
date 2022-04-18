from Screen.client import Client
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_INPUT = (Configurations.SERVER_IP, 5002)

if __name__ == "__main__":
    receiver = Client(ADDRESS, ADDRESS_INPUT, "Live")
    receiver.start()
