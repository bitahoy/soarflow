import aiohttp
import asyncio

# example
# https://opensearch.org/docs/latest/opensearch/popular-api/

class OpenSearchConnection:

    def __init__(self, base_url):
        self.base_url = base_url

    async def get_search_results(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url) as resp:
                return await resp.json()

async def main():
    print('Hello, world!')
    conn = OpenSearchConnection('https://admin:admin@localhost:9200/')
    print(await conn.get_search_results())


asyncio.run(main())