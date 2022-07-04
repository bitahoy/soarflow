import json
from scapy.all import *
from scapy.layers.dns import DNS
from jsonPacket import pkt2dict
from opensearch import OpenSearchConnection


class Imports:

    """
    A class to import data from various import format int o OpenSearch
    """

    def __init__(self, opensearchconnection: OpenSearchConnection):
        self.opensearchconnection = opensearchconnection

    async def importFromPcap(self, pcaplocation, indexname="pcap-0"):
        """
        Import a PCAP file into OpenSearch

        :param pcaplocation: The PCAP file to import
        :param indexname: The name of the index to create
        :return: The response from the OpenSearch server
        """
        scapy_cap = rdpcap(pcaplocation)
        indexname, indexversion = indexname.rsplit("-",1)
        await self.opensearchconnection.create_index(indexname+"-"+indexversion, {
    "mappings": {
    "properties": {
        "@timestamp": {
        "type": "date"
        },
    }
  }
    }, True)
        upload = []
        i = 0
        out = ""
        for packet in scapy_cap:
            if True:
                
                d = pkt2dict(packet)
                d["@timestamp"] = int(float(packet.time) * 1000)
                upload.append(d)
                if i > 500:
                    print(f"uploading {i}")
                    out += str(await self.opensearchconnection.add_documents(indexname+"-"+indexversion, upload)) + "\n"
                    upload = []
                    i = 0
                i += 1
        return "\n" + str(await self.opensearchconnection.add_documents(indexname+"-"+indexversion, upload))

    async def importFromCsv(self, csv: str, indexname="csv-0"):
        """
        Import a CSV file into OpenSearch

        :param csv: The CSV file to import
        :param indexname: The name of the index to create
        :return: The response from the OpenSearch server
        """
        indexname, indexversion = indexname.rsplit("-",1)
        header, body = csv.split("\n", 1)
        headers = header.split(",")
        items = []
        for line in body.split("\n"):
            if line == "":
                continue
            d = {}
            for i, h in enumerate(headers):
                d[h] = line.split(",")[i]
            if "time" in d:
                d["@timestamp"] = int(float(d["time"]) * 1000)
            items.append(d)

            
        indexname = indexname + "-" + indexversion
        

        await self.opensearchconnection.create_index(indexname, {
    "mappings": {
    "properties": {
        "@timestamp": {
        "type": "date"
        },
    }
  }
    }, True)
        return "\n" + str(await self.opensearchconnection.add_documents(indexname, items))


    async def importFromJson(self, body: str, indexname="json-0"):
        """
        Import a JSON file into OpenSearch

        :param body: The JSON file to import
        :param indexname: The name of the index to create
        :return: The response from the OpenSearch server
        """
        indexname, indexversion = indexname.rsplit("-",1)
        body = body.strip("\n")
        items = []
        for line in body.split("\n"):
            d = json.loads(line)
            if "@timestamp" in d:
                d["@timestamp"] = int(float(d["@timestamp"]))
            items.append(d)

            
        indexname = indexname + "-" + indexversion
        

        await self.opensearchconnection.create_index(indexname, {
    "mappings": {
    "properties": {
        "@timestamp": {
        "type": "date"
        },
    }
  }
    }, True)
        return "\n" + str(await self.opensearchconnection.add_documents(indexname, items))