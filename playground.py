import asyncio
import os
import time
import pickle
import zmq.asyncio
import zmq.sugar
from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
import uvloop


async def inf():
    while True:
        await asyncio.sleep(1)


async def mian():
    g = asyncio.gather(inf(), inf())
    if g.done():
        print("Hello")
    else:
        print("Nope")
        g.cancel()
        await g
        if g.done():
            print("Ok")
        else:
            print("rau")

if __name__ == "__main__":
    asyncio.run(mian())
