import asyncio
import zmq.asyncio


async def respond(sock, msg):
    while True:
        await sock.recv()
        sock.send_string(msg)


async def main():
    c = zmq.asyncio.Context()
    s0 = c.socket(zmq.REP)
    s0.bind("tcp://*:5002")

    s1 = c.socket(zmq.REP)
    s1.bind("tcp://*:5003")

    s2 = c.socket(zmq.REQ)
    s2.connect("tcp://localhost:5002")
    s2.connect("tcp://localhost:5003")

    t = asyncio.gather( respond(s0, "Hello"), respond(s1, "5"),)

    s2.send(b"0")
    s2.send(b"0")
    print(await s2.recv())
    print(await s2.recv())

    await t

if __name__ == "__main__":
    asyncio.run(main())




