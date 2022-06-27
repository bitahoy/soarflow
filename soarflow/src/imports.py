from scapy.all import *
from scapy.layers.dns import DNS
from src.jsonPacket import JsonPacket
from src.opensearch import OpenSearchConnection

class Imports:

    async def importFromPcap(self, pcaplocation):
        scapy_cap = rdpcap(pcaplocation)
        jsonp = JsonPacket()
        opensearchcon = OpenSearchConnection("http://127.0.0.1:5601/")
        #opensearchcon.create_index("test")
        for packet in scapy_cap:
            if(packet.haslayer(DNS)):
                jsondmp = jsonp.pkt2dict(packet)
                print(jsondmp)
                opensearchcon.add_document("test", jsondmp)
                #if(packet.qdcount > 0 and isinstance(packet.qd, DNSQR)):
                #    name = packet.qd.qname
                #elif(packet.ancount > 0 and isinstance(packet.an, DNSRR)):
                #    name = packet.an.rdata
                #else:
                #    continue

                #print(name)

