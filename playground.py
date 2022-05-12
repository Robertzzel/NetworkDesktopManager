import zmq.asyncio
import asyncio
from random import randint

async def consumer(q):
    while True:
        print(await q.get())
        q.task_done()

async def producer(q):
    while True:
        await q.put(randint(0, 10))
        await asyncio.sleep(1)

async def main():
    q = asyncio.Queue(2)
    t1 = asyncio.create_task(producer(q))
    t2 = asyncio.create_task(consumer(q))
    await t1
    await t2

if __name__ == "__main__":
    asyncio.run(main(), debug=True)