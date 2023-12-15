import asyncio

def exitAsyncio():
    loop = asyncio.get_event_loop()
    loop.stop() 