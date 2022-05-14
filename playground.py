import asyncio
import os
import zmq.asyncio
import zmq.sugar


async def push_hello(sock: zmq.sugar.Socket):
    while True:
        print("Creez")
        sock.send_string("Hello")
        await asyncio.sleep(1)


async def push_welcome(sock: zmq.sugar.Socket):
    while True:
        sock.send_string("wellcome")
        await asyncio.sleep(1)


async def main():
    context = zmq.asyncio.Context()
    poller = zmq.asyncio.Poller()

    s0, s1, s2 = context.socket(zmq.PULL), context.socket(zmq.PUSH), context.socket(zmq.PUSH)
    s0.bind("ipc:///tmp/proiectz_mq/0")
    s1.connect("ipc:///tmp/proiectz_mq/0")
    s2.connect("ipc:///tmp/proiectz_mq/0")

    poller.register(s0, zmq.POLLIN)

    task = asyncio.gather(push_welcome(s1), push_hello(s2))

    while True:
        p = dict(await poller.poll())
        if s0 in p:
            print(await s0.recv())

    await task

if __name__ == "__main__":
    asyncio.run(main())