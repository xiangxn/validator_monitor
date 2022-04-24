import json
import psutil
import asyncio
import subprocess
import os
from validator_monitor.discord_bot import DiscordBot
from validator_monitor.logger import Logger

GB = 1024**3


class Server:

    def __init__(self, config, debug=False) -> None:
        self.config = config
        self.logger = Logger("monitor", debug=debug)
        self.discord_bot = DiscordBot(self.config, self.logger)
        self.info = {
            "latest_block_height": 0,
            "data": "0",
            "disk": "",
            "cpu": "",
            "memory": "",
            "jailed": False,
            "delegator_shares": "",
            "rewards": "",
            "balance": "",
            "active": False
        }

    async def get_device(self):
        # logs
        r = os.popen(f"du -h -d1 {self.config['work_dir']}")
        lines = r.readlines()
        for line in lines:
            if "/data" in line:
                self.info['data'] = line.split("\t")[0].strip()
                break
        # disk
        disk_info = psutil.disk_usage(self.config['work_dir'])
        self.info['disk'] = f"total: {disk_info.total/GB:.2f}GB, used: {disk_info.used/GB:.2f}GB, free: {disk_info.free/GB:.2f}GB"
        # cpu
        cpu_percent = psutil.cpu_percent(interval=1)
        self.info['cpu'] = f"{cpu_percent}%"
        # memory
        memory = psutil.virtual_memory()
        self.info['memory'] = f"total: {memory.total/GB:.2f}GB used: {(memory.total-memory.available)/GB:.2f}GB, percent: {memory.percent}%"
        # print(self.info)

    async def get_service(self):
        output = subprocess.getoutput("./scripts/balance.sh")
        if output and output.startswith('{"balances":'):
            obj = json.loads(output)
            self.info['balance'] = f"{(float(obj['balances'][0]['amount']) / 1000000):.6f} ATOM"
        output = subprocess.getoutput("./scripts/distribution.sh")
        if output and output.startswith('{"rewards":'):
            obj = json.loads(output)
            self.info['rewards'] = f"{(float(obj['rewards'][0]['amount']) / 1000000):.6f} ATOM"
        output = subprocess.getoutput("./scripts/validator.sh")
        if output and output.startswith('{"operator_address":'):
            obj = json.loads(output)
            self.info['delegator_shares'] = f"{(float(obj['delegator_shares'])/1000000):.6f} ATOM"
            self.info['jailed'] = obj['jailed']
        output = subprocess.getoutput("./scripts/vstatus.sh")
        if output and output.startswith('- address:'):
            self.info['active'] = True
        # print(self.info)

    async def get_sync_block(self):
        output = subprocess.getoutput("./scripts/nstatus.sh")
        if output and output.startswith('{"NodeInfo":'):
            obj = json.loads(output)
            self.info['latest_block_height'] = obj['SyncInfo']['latest_block_height']

        # print(self.info)

    async def read_info(self):
        while True:
            await self.get_device()
            await self.get_service()
            await self.get_sync_block()
            true = "🟢"
            false = "🔴"
            msg = f"""
            {self.config['title']}:
            -----------------------------------------------
            Latest block height: {self.info['latest_block_height']}
            -----------------------------------------------
            Data size: {self.info['data']}
            -----------------------------------------------
            Disk: {self.info['disk']}
            CPU: {self.info['cpu']}
            Memory: {self.info['memory']}
            -----------------------------------------------
            Active: {true if self.info['active'] else false}
            Jailed: {"🆘" if self.info['jailed'] else "😎"}
            Delegator shares: {self.info['delegator_shares']}
            Balance: {self.info['balance']}
            Rewards: {self.info['rewards']}
            """
            self.discord_bot.push_message(msg)
            await asyncio.sleep(self.config['check_interval'])

    def get_tasks(self, loop: asyncio.AbstractEventLoop):
        return [loop.create_task(self.read_info())]

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.get_tasks(loop)))
        loop.close()