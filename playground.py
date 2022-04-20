import asyncio
from threading import Thread


async def ceva():
    await asyncio.sleep(1)
    print("S-a dus o sec")

async def main():
    pass

if __name__ == "__main__":
    task = asyncio.create_task(ceva())
    for i in range(10000):
        print("main")

    await task