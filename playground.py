import zmq
import asyncio


async def send(socket):
    socket = zmq.Context().socket(zmq.REQ)
    socket.bind(f"tcp://*:{5001}")
    socket.send(b"sal")


async def sleep():
    await asyncio.sleep(3)
    print("gata sleepul")

async def main():
    socket = zmq.Context().socket(zmq.DEALER)
    socket.bind(f"tcp://*:{5002}")

    t1 = asyncio.create_task(send(socket))
    t2 = asyncio.create_task(sleep())
    await t2
    await t1


if __name__ == "__main__":
    asyncio.run(main())

