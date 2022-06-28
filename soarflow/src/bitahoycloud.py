from datetime import datetime
import websockets
import aiohttp
import asyncio
import json
from opensearch import OpenSearchConnection
import os



async def get_auth_token(email=None, password=None):
  if not email:
    email = os.environ.get("BITAHOY_EMAIL")
  if not password:
    password = os.environ.get("BITAHOY_PASSWORD")
  async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
      async with session.post("https://auth.bitahoy.cloud/login", json={"email": email, "password": password}) as resp:
          return (await resp.json())["token"]


async def poll_blocked_domains(token, conn, entries=[None]):
    if entries[0] is None:
      entries[0] = 0
    # conn = OpenSearchConnection('https://admin:admin@localhost:9200/')
    print(await conn.create_index('contentblocking', {
        
  "mappings": {
    "properties": {
      "domain": {
        "type": "text"
      },
      "category": {
        "type": "text"
        },
        "reason": {
        "type": "text"
        },
        "source": {
        "type": "text"
        },
        "blocked": {
        "type": "boolean"
        },
        "@timestamp": {
        "type": "date"
        },
        "time": {
        "type": "date",
        },
    }
  }
    }))
    async with websockets.connect("wss://contentblocking.bitahoy.cloud/ws") as websocket:
        await websocket.send(json.dumps({"action": "auth", "token": token}))
        await websocket.recv()
        lastid = 0
        while True:
            await websocket.send(json.dumps({"action": "get_data_detailed", "id": lastid}))
            message = json.loads(await websocket.recv())
            print(f"pulled {len(message['detailed'])} new records")
            entries[0] += len(message['detailed'])
            items = []
            for item in message["detailed"]:
                lastid = max(lastid, item["id"])
                index = item["id"]
                item["@timestamp"] = item["time"] * 1000
                item["_id"] = index

                del item["id"]
                items.append(item)
                if len(items) >= 100:
                    resp = await conn.add_documents('contentblocking', items)
                    print(resp)
                    items = []
            if len(items) > 0:
                message = await conn.add_documents('contentblocking', items)
                print(message)
            await asyncio.sleep(10)


# async def main():
#     token = await get_auth_token()
#     await poll_blocked_domains(token)


# asyncio.run(main())