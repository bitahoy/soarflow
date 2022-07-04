import aiohttp
import json

class OpenSearchConnection:
    """
    Class for interacting with the OpenSearch API
    """

    def __init__(self, base_url):
        self.base_url = base_url.strip("/")

    async def get_search_results(self):
        """
        Get the results of a search

        :return: The results of the search
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url) as resp:
                return await resp.json()

    async def get_index_settings(self, index_name):
        """
        Get the settings of an index

        :param index_name: The name of the index
        :return: The settings of the index
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url + "/" + index_name + "/_settings") as resp:
                return await resp.json()

    async def get_index_mappings(self, index_name):
        """
        Get the mappings of an index
        
        :param index_name: The name of the index
        :return: The mappings of the index
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(self.base_url + "/" + index_name + "/_mapping") as resp:
                return await resp.json()

    async def create_index(self, index_name, settings={}, override=False):
        """
        Create an index

        :param index_name: The name of the index
        :param settings: The settings of the index
        :param override: Whether to override the index if it already exists
        :return: The results of the index creation
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            mappings = await self.get_index_mappings(index_name)
            if not override and index_name in mappings:
                return mappings[index_name]
            elif override:
                await self.delete_index(index_name)
            async with session.put(self.base_url + "/" + index_name, json=settings) as resp:
                return await resp.json()

    async def delete_index(self, index_name):
        """
        Delete an index

        :param index_name: The name of the index
        :return: The results of the index deletion
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.delete(self.base_url + "/" + index_name) as resp:
                return await resp.json()

    async def add_document(self, index_name, document, index=None):
        """
        Add a document to an index
        
        :param index_name: The name of the index
        :param document: The document to add
        :param index: The index to add the document to
        :return: The results of the document addition
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            if index is None:
                async with session.post(self.base_url + "/" + index_name + "/_doc", json=document) as resp:
                    return await resp.json()
            else:
                async with session.post(self.base_url + "/" + index_name + "/_doc/" + str(index), json=document) as resp:
                    return await resp.json()

    async def add_documents(self, index_name, documents):
        """
        Add multiple documents to an index

        :param index_name: The name of the index
        :param documents: The documents to add
        :return: The results
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            data = ""
            for document in documents:
                header = {"index": {}}
                if "_id" in document:
                    header["index"]["_id"] = document["_id"]
                    del document["_id"]
                data += json.dumps(header) + "\n"
                try:
                    data += json.dumps(document) + "\n"
                except TypeError as e:
                    print(document)
                    raise e

            async with session.post(self.base_url + "/" + index_name + "/_bulk", data=data, headers={'content-type':'application/json', 'charset':'UTF-8'}) as resp:
                return await resp.json()

    async def create_template(self, template_name, template):
        """
        Create a template

        :param template_name: The name of the template
        :param template: The template to create
        :return: The results of the template creation
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.put(self.base_url + "/_template/" + template_name, json=template) as resp:
                return await resp.json()