import socket
from Screen.screen_receiver import ScreenReceiver
from Commons.computer import Computer

ADDRESS = (Computer.get_wifi_ip_address(), 5001)

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(ADDRESS)

    receiver = ScreenReceiver(sock, "Live")
    receiver.start_receiving()
