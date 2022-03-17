import asyncio
import websockets
import json

async def hello():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("heelo")
        data = await websocket.recv()
        print(data)

asyncio.get_event_loop().run_until_complete(hello())
