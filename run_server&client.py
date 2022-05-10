from subprocess import Popen
from sys import executable
import run_client
import run_server
import time
import signal


if __name__ == "__main__":

    try:
        receiver_process = Popen([executable, run_client.__file__])
        time.sleep(1)
        sender_process = Popen([executable, run_server.__file__])
        time.sleep(1)
        input()
    except:
        pass
    else:
        receiver_process.send_signal(signal.SIGINT)
        sender_process.send_signal(signal.SIGINT)
        time.sleep(3)
        receiver_process.kill()
        sender_process.kill()

