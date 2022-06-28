from __future__ import print_function
from scapy.packet import Packet, NoPayload
from scapy.fields import FlagValue

def pkt2dict(pkt):
    if isinstance(pkt, NoPayload):
        return {}
    elif isinstance(pkt, FlagValue):
        return pkt2dict(pkt.value)
    elif isinstance(pkt, Packet):
        d = {}
        for f in pkt.fields_desc:
            if f.name in pkt.fields:
                d[f.name] = pkt2dict(pkt.fields[f.name])
        if pkt.payload is not None and pkt.payload.__class__ != NoPayload:
            d[pkt.payload.name] = pkt2dict(pkt.payload)
        return d
    elif isinstance(pkt, list):
        return [pkt2dict(i) for i in pkt]
    elif isinstance(pkt, tuple):
        return tuple([pkt2dict(i) for i in pkt])
    elif isinstance(pkt, str):
        return pkt
    elif isinstance(pkt, int):
        return pkt
    elif isinstance(pkt, float):
        return pkt
    elif isinstance(pkt, bytes):
        try:
            return pkt.decode()
        except UnicodeDecodeError:
            return "<binary>"
    elif isinstance(pkt, dict):
        d = {}
        for k, v in pkt.items():
            d[k] = pkt2dict(v)
        return d
    elif isinstance(pkt, set):
        return [pkt2dict(i) for i in pkt]
    elif isinstance(pkt, bool):
        return pkt
    elif isinstance(pkt, type(None)):
        return None
    else:
        return repr(pkt)