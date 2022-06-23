import os
import subprocess
import aiohttp
import asyncio
import time
import shlex


class Exports:

    async def exportBulk(self, json):
        cmd = '''curl -k -X POST 'https://admin:admin@localhost:9200''' + json
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

