from datetime import datetime
import websockets
import aiohttp
import asyncio
import json
import os


"""
A set of functions to interact with the Bitahoy Cloud API.

https://www.bitahoy.com/
"""



async def get_auth_token(email=None, password=None):
  """
  Get an auth token from the Bitahoy Cloud API.
  """
  if not email:
    email = os.environ.get("BITAHOY_EMAIL")
  if not password:
    password = os.environ.get("BITAHOY_PASSWORD")
  async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
      async with session.get("https://auth.bitahoy.cloud/", timeout=10) as resp:
        print(await resp.text())
      async with session.post("https://auth.bitahoy.cloud/login", json={"email": email, "password": password}, timeout=10) as resp:
          return (await resp.json())["token"]


async def poll_blocked_domains(token, conn, entries=[None]):
  """
  Poll the Bitahoy Cloud API for blocked domains. The data originates from the content-blocking addon.

  :param token: The auth token (obtained from get_auth_token)
  :param conn: The websocket connection
  :param entries: A list of ints. entries[0] will be always updated with the number of entries synced
  :return: SHOULD NEVER RETURN, its a backgrund task.
  """
  if entries[0] is None:
    entries[0] = 0
  print(await conn.create_index('contentblocking', {
        "mappings": {
          "properties": {
            "domain": {
              "type": "keyword"
            },
            "category": {
              "type": "keyword"
              },
              "reason": {
              "type": "keyword"
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
          await websocket.send(json.dumps({"action": "get_data_detailed", "id": lastid, "show_benign": True}))
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