import websockets
import aiohttp
import asyncio
import json
from opensearch import OpenSearchConnection
import sys



async def get_auth_token():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post("https://auth.bitahoy.cloud/login", json={"email": sys.argv["BITAHOY_USER"], "password": sys.argv["BITAHOY_PASS"]}) as resp:
            return (await resp.json())["token"]


async def poll_blocked_domains(token):
    conn = OpenSearchConnection('https://admin:admin@localhost:9200/')
    await conn.create_index('contentblocking')
    async with websockets.connect("wss://contentblocking.bitahoy.cloud/ws") as websocket:
        await websocket.send(json.dumps({"action": "auth", "token": token}))
        await websocket.recv()
        lastid = 0
        while True:
            await websocket.send(json.dumps({"action": "get_data_detailed", "id": lastid}))
            message = json.loads(await websocket.recv())
            for item in message["detailed"]:
                lastid = max(lastid, item["id"])
                index = item["id"]
                item["@timestamp"] = item["time"]
                del item["id"]
                message = await conn.add_document('contentblocking', item, index)
                print(message)
            await asyncio.sleep(10)


async def main():
    token = await get_auth_token()
    await poll_blocked_domains(token)


asyncio.run(main())