from Screen.client import Client
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)

if __name__ == "__main__":
    receiver = Client(ADDRESS, "Live")
    receiver.start()
