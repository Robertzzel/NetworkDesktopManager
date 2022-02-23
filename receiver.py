from Screen.screen_receiver import ScreenReceiver
from Commons.computer import Computer

ADDRESS = (Computer.get_wifi_ip_address(), 5001)
ADDRESS_MOUSE = (Computer.get_wifi_ip_address(), 5002)

if __name__ == "__main__":
    receiver = ScreenReceiver(ADDRESS, ADDRESS_MOUSE, "Live")
    receiver.start()
