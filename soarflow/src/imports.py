import json
from scapy.all import *
from scapy.layers.dns import DNS
from jsonPacket import pkt2dict
from opensearch import OpenSearchConnection


def object_sanitizer(o):
    if isinstance(o, bytes):
        try:
            return o.decode()
        except UnicodeDecodeError:
            "<binary>"
    elif isinstance(o, dict):
        d2 = {}
        for k, v in o.items():
            d2[k] = object_sanitizer(v)
        return d2
    elif isinstance(o, list):
        l2 = []
        for i in o:
            l2.append(object_sanitizer(i))
        return l2
    elif isinstance(o, tuple):
        l2 = []
        for i in o:
            l2.append(object_sanitizer(i))
        return tuple(l2)
    else:
        return o



class Imports:

    def __init__(self, opensearchconnection: OpenSearchConnection):
        self.opensearchconnection = opensearchconnection

    async def importFromPcap(self, pcaplocation, indexname="pcap"):
        scapy_cap = rdpcap(pcaplocation)
        indexname, indexversion = indexname.rsplit("-",1)
        # res = await self.opensearchconnection.create_template(indexname+"-", {
        #     "index_patterns": [indexname+"-*"],
        #     "mappings": {
        #         "_source": {
        #             "enabled": False
        #         },
        #         "properties": {
        #             "@timestamp": {
        #                 "type": "date",
        #                 "index": True,
        #             }
        #         }
        #     }

        # })
        print(res)
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
            if True: #(packet.haslayer(DNS)):
                
                d = pkt2dict(packet)
                d["@timestamp"] = int(float(packet.time) * 1000)
                d = object_sanitizer(d)
                upload.append(d)
                if i > 500:
                    print(f"uploading {i}")
                    out += str(await self.opensearchconnection.add_documents(indexname+"-"+indexversion, upload)) + "\n"
                    upload = []
                    i = 0
                i += 1
        return "\n" + str(await self.opensearchconnection.add_documents(indexname+"-"+indexversion, upload))

    async def importFromCsv(self, csv: str, indexname="csv"):
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


    async def importFromJson(self, body: str, indexname="json"):
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