# Import: JSON; PCAP, netflow (v9)

Assign: Hendrik, Anonymous
Date Created: June 14, 2022 4:55 PM
Status: In Progress

@Hendrik 

Regarding the NetFlow import, this is the lib that I mentioned: [https://www.notion.so/bitahoy/Dummy-input-data-f5292a7bc6504ea49afe7090147fd53f](https://www.notion.so/Dummy-input-data-f5292a7bc6504ea49afe7090147fd53f)

```json

or with cloudjet:
sudo tcpdump -i enx083a885743d4 -l -n --immediate-mode udp port 6666 -xxx
```

Working NETFLOW setup to work on this locally:

1. https://github.com/TamalTanuDatta/netflowGenerator (alternately, you could use softflowd to format pcap to netflowv5)
2. [https://github.com/bitkeks/python-netflow-v9-softflowd](https://github.com/bitkeks/python-netflow-v9-softflowd/tree/06d7c0c5d083415ffff2f34cb905f04e6d999cdf)

How to use:

1. First setup a listener using the CLI for the collector python netflow lib: 
2. if you run locally you do not need to state an ip. I choose port 6666 in this case, but feel free to switch.

```json
python3 -m netflow.collector --port 6666 -D
```

1. Now setup the generator: simply download the binary for `./nflow-generator` : [https://github.com/nerdalert/nflow-generator/blob/master/binaries/nflow-generator-x86_64-linux](https://github.com/nerdalert/nflow-generator/blob/master/binaries/nflow-generator-x86_64-linux)
2. This can can be used to start a dummy generator on a certain port, in my case with my local ip: 

```json
	./nflow-generator -t 127.0.0.1 -p 6666
```

1. You should see data on the listener, like:

```json
~/D/B/python-netflow-v9-softflowd ❯❯❯ python3 -m netflow.collector --port 6666 -D                                                                                                                      ✘ 2 master ◼
2022-06-21 15:25:28,723 - INFO - Starting the NetFlow listener on 0.0.0.0:6666
2022-06-21 15:25:32,043 - DEBUG - Received 792 bytes of data from ('172.30.37.246', 41961)
2022-06-21 15:25:32,043 - DEBUG - Processed a v5 ExportPacket with 16 flows.
2022-06-21 15:25:32,740 - DEBUG - Received 792 bytes of data from ('172.30.37.246', 41961)
2022-06-21 15:25:32,740 - DEBUG - Processed a v5 ExportPacket with 16 flows.
2022-06-21 15:25:33,436 - DEBUG - Received 792 bytes of data from ('172.30.37.246', 41961)
2022-06-21 15:25:33,436 - DEBUG - Processed a v5 ExportPacket with 16 flows.
2022-06-21 15:25:36,559 - DEBUG - Received 792 bytes of data from ('172.30.37.246', 41961)
2022-06-21 15:25:36,559 - DEBUG - Processed a v5 ExportPacket with 16 flows.
^C2022-06-21 15:25:39,239 - DEBUG - Received signal 2, raising StopIteration
2022-06-21 15:25:39,239 - INFO - Shutting down the NetFlow listener	
```

1. It will dump it into a .gz file in the folder, but inside you can find the serialized JSON data for Netflow v5(!!!):
2. 

```json
~/D/B/python-netflow-v9-softflowd ❯❯❯ head -n 1 1655817793                                                                                                                                                 master ◼
{"1655817798.8633146": {"client": ["172.30.37.246", 47524], "header": {"version": 5, "count": 16, "uptime": 1000, "timestamp": 1655817798, "timestamp_nano": 862798141, "sequence": 1, "engine_type": 1, "engine_id": 0, "sampling_interval": 0}, "flows": [{"IPV4_SRC_ADDR": 1879708682, "IPV4_DST_ADDR": 2887695882, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 921, "IN_OCTETS": 919, "FIRST_SWITCHED": 389, "LAST_SWITCHED": 628, "SRC_PORT": 40, "DST_PORT": 80, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 19666, "DST_AS": 52270, "SRC_MASK": 3, "DST_MASK": 12}, {"IPV4_SRC_ADDR": 3232240650, "IPV4_DST_ADDR": 3389832714, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 452, "IN_OCTETS": 13, "FIRST_SWITCHED": 702, "LAST_SWITCHED": 910, "SRC_PORT": 40, "DST_PORT": 443, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 59455, "DST_AS": 45777, "SRC_MASK":
```

Dummy JSON data from dummy netflow v5:

[1655817793](Import%20JSON;%20PCAP,%20netflow%20(v9)%2025b1eb9a906d4ec3ba941e9b8eb77998/1655817793.txt)