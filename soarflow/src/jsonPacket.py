from __future__ import print_function
from scapy.packet import Packet
from collections import defaultdict
import json

class JsonPacket(Packet):

    def pkt2dict(self, pkt):
        packet_dict = {}
        for line in pkt.show2(dump=True).split('\n'):
            if '###' in line:
                if '|###' in line:
                    sublayer = line.strip('|#[] ')
                    packet_dict[layer][sublayer] = {}
                else:
                    layer = line.strip('#[] ')
                    packet_dict[layer] = {}
            elif '=' in line:
                if '|' in line and 'sublayer' in locals():
                    key, val = line.strip('| ').split('=', 1)
                    packet_dict[layer][sublayer][key.strip()] = val.strip('\' ')
                else:
                    key, val = line.split('=', 1)
                    val = val.strip('\' ')
                    if (val):
                        try:
                            packet_dict[layer][key.strip()] = eval(val)
                        except:
                            packet_dict[layer][key.strip()] = val
            else:
                print("pkt2dict packet not decoded: " + line)
        return packet_dict