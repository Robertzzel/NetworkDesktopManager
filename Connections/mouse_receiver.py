from Commons.mouse_tool import MouseTool
import socket


class MouseReceiver:
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection: socket.socket = None

    def connect(self):
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()

    def start_receiving(self):
        while True:
            data = self._sender_connection.recv(32).decode()
            self._sender_connection.sendall(b"X")

            action, details = data.split(":")
            if action == "click":
                button, pressed = details.split(",")
                if details == "Button.left":
                    if pressed:
                        self._mouse_tool.left_press()
                    else:
                        self._mouse_tool.left_release()
                elif details == "Button.right":
                    if pressed:
                        self._mouse_tool.right_press()
                    else:
                        self._mouse_tool.right_release()
                else:
                    print("click necunoscut")
            elif action == "move":
                print("MOVE")
            else:
                print("action 404")



