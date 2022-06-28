import aiohttp
import json

class OpenSearchConnection:

    def __init__(self, base_url):
        self.base_url = base_url.strip("/")

    async def get_search_results(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url) as resp:
                return await resp.json()

    async def get_index_settings(self, index_name):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url + "/" + index_name + "/_settings") as resp:
                return await resp.json()

    async def get_index_mappings(self, index_name):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url + "/" + index_name + "/_mapping") as resp:
                return await resp.json()

    async def create_index(self, index_name, settings={}, override=False):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            mappings = await self.get_index_mappings(index_name)
            if not override and index_name in mappings:
                return mappings[index_name]
            elif override:
                await self.delete_index(index_name)
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

    async def add_documents(self, index_name, documents):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            data = ""
            for document in documents:
                header = {"index": {}}
                if "_id" in document:
                    header["index"]["_id"] = document["_id"]
                    del document["_id"]
                data += json.dumps(header) + "\n"
                data += json.dumps(document) + "\n"
                

            async with session.post(self.base_url + "/" + index_name + "/_bulk", data=data, headers={'content-type':'application/json', 'charset':'UTF-8'}) as resp:
                return await resp.json()