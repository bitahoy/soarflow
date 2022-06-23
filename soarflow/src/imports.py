import os
import subprocess
import aiohttp
import asyncio
import time
import shlex


class Imports:

    async def importFromPcap(self, pcaplocation):
        timestamp = str(time.time())
        newpath = "./../json/" + timestamp
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        cmd = "cat " + pcaplocation + " | ./../util/pcap2json --json-packet"
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

