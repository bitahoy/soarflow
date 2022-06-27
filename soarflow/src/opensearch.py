import aiohttp
import json

class OpenSearchConnection:

    def __init__(self, base_url):
        self.base_url = base_url.strip("/")

    async def get_search_results(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url) as resp:
                return await resp.json()

    async def create_index(self, index_name, settings={}):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.put(self.base_url + "/" + index_name, json=settings) as resp:
                return await resp.json()

    async def delete_index(self, index_name):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.delete(self.base_url + "/" + index_name) as resp:
                return await resp.json()

    async def add_document(self, index_name, document, index=None):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            if index is None:
                async with session.post(self.base_url + "/" + index_name + "/_doc", json=document) as resp:
                    return await resp.json()
            else:
                async with session.post(self.base_url + "/" + index_name + "/_doc/" + str(index), json=document) as resp:
                    return await resp.json()