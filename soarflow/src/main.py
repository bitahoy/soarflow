import asyncio
from imports import *
import time
from opensearch import OpenSearchConnection

# example
# https://opensearch.org/docs/latest/opensearch/popular-api/




async def main():
    print('Hello, world!')
    #imports = Imports
    #await imports.importFromPcap(imports, "/home/hacker/Downloads/18-06-14.pcap")
    conn = OpenSearchConnection('https://admin:admin@localhost:9200/')

    print(await conn.create_index('test'))

    resp = await conn.add_document('test', {
                "domain": "siem.testing.bitahoy.com",
                "@timestamp": time.time(),
                "category": "ads",
                "reason": "test",
                "source": "127.0.0.1",
                "blocked": True,
            })
    print(resp)
    print(await conn.get_search_results())

asyncio.run(main())
