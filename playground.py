import zmq
import asyncio

if __name__ == "__main__":
    sock = zmq.Context().socket(zmq.PAIR)
    sock.bind("tcp://*:5002")

    try:
        while True:
            print(sock.recv_string())
    except:
        print("sending")
        sock.send(b"1")