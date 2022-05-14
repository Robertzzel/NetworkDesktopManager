#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq

#  Prepare our context and sockets
context = zmq.Context()
socket1 = context.socket(zmq.REQ)
socket1.connect("tcp://localhost:5559")

socket2 = context.socket(zmq.REP)
socket2.connect("tcp://localhost:5560")

socket3 = context.socket(zmq.REP)
socket3.connect("tcp://localhost:5560")

frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:5559")
backend.bind("tcp://*:5560")

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

def start_socket1():
    #  Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        socket1.send(b"Hello")
        message = socket1.recv()
        print(f"Received reply {request} [{message}]")

def start_socket2():
    while True:
        message = socket2.recv()
        print(f"Received request: {message}")
        socket2.send(b"World")

def start_socket2_2():
    while True:
        message = socket2.recv()
        print(f"Received request: {message}")
        socket2.send(b"NoWorld")


def start_broker():
    while True:
        socks = dict(poller.poll())

        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv_multipart()
            backend.send_multipart(message)

        if socks.get(backend) == zmq.POLLIN:
            message = backend.recv_multipart()
            frontend.send_multipart(message)

from threading import Thread
Thread(target=start_broker).start()
Thread(target=start_socket1).start()
Thread(target=start_socket2).start()
#Thread(target=start_socket2_2).start()








