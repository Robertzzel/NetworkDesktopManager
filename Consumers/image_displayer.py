from Commons.image_operations import ImageOperations
from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey, destroyAllWindows
from configurations import Configurations
import zmq, sys


class ImageDisplayer:
    def __init__(self, port):
        self._socket = zmq.Context().socket(zmq.PAIR)
        self._socket.connect(f"tcp://localhost:{port}")

    def start(self):
        try:
            namedWindow(Configurations.WINDOW_NAME, WINDOW_NORMAL)

            while True:
                action = self._socket.recv()
                if action == b"0":
                    imshow(Configurations.WINDOW_NAME,
                           ImageOperations.decode(self._socket.recv_pyobj()))
                    waitKey(1)
                elif action == b"1":
                    destroyAllWindows()
                    break
        except:
            print("Displayer oprit")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ImageDisplayer(sys.argv[1]).start()
    else:
        print("No port given")
