from Commons.mouse_tool import MouseTool
from Connections.ImageConnections.image_sender import ImageSender
from Connections.base_connection import BaseConnection
from configurations import Configurations
from Commons.keyboard_tool import KeyboardTool
from socket import socket, AF_INET, SOCK_STREAM
from Commons.input_actions import InputActions
from threading import Thread


class InputReceiver(BaseConnection):

    def __init__(self, address):
        self._mouse = MouseTool()
        self._keyboard = KeyboardTool()
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection = None

        self.click_mapper = {
            "Button.leftTrue": self._mouse.left_press,
            "Button.leftFalse": self._mouse.left_release,
            "Button.rightTrue": self._mouse.right_press,
            "Button.rightFalse": self._mouse.right_release
        }

    def connect(self):
        print(f"Keyboard:Listening at {self._address}")
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()
        print(f"Connected to {self._sender_connection}")

    def start(self):
        Thread(target=self._start_receiving).start()

    def _start_receiving(self):
        while True:
            data = self.receive_message(self._sender_connection, Configurations.INPUT_MAX_SIZE).decode()
            action, details = data.split(":")
            action = InputActions(int(action))

            if action == InputActions.MOVE:
                x, y = details.split(",")
                ImageSender.CURSOR_POSITIONS = (int(x), int(y))
            elif action == InputActions.PRESS:
                print("press" + details)
                self._keyboard.press_letter(details)
            elif action == InputActions.RELEASE:
                print("release" + details)
                self._keyboard.release_letter(details)
            elif action == InputActions.CLICK:
                self.click_mapper[details]()
            else:
                print("action 404")
