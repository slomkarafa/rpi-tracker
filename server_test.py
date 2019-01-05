import asyncio
import websockets
import time


async def mock_steering(uri):
    async with websockets.connect(f'{uri}/go') as w:
        await w.send("100 100")
        await w.send("50 50")
        await w.send('stop')
        # await w.send(f'{uri}/s')


def test():
    asyncio.get_event_loop().run_until_complete(mock_steering('ws://0.0.0.0:8080'))


if __name__ == '__main__':
    test()
