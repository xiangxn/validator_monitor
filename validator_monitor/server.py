import psutil
import asyncio
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
            "tokens": "",
            "balance": "",
            "restful": False
        }

    async def get_device(self):
        # logs
        r = os.popen(f"du -h -d1 {self.config['work_dir']}")
        lines = r.readlines()
        for line in lines:
            if "/logs\n" in line:
                self.info['logs'] = line.split("\t")[0].strip()
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
        r = os.popen("./scripts/nstatus.sh")
        lines = r.readlines()
        for line in lines:
            if "datacenter_sync_1" in line:
                self.info['sync'] = False if " Exited " in line else True
            if "datacenter_mongo_1" in line:
                self.info['mongo'] = False if " Exited " in line else True
            if "datacenter_grpc_1" in line:
                self.info['grpc'] = False if " Exited " in line else True
            if "datacenter_restful_1" in line:
                self.info['restful'] = False if " Exited " in line else True
            if "datacenter_graphql_1" in line:
                self.info['graphql'] = False if " Exited " in line else True
        # print(self.info)

    async def get_sync_block(self):
        block = "0"
        line = ""
        while block == "0":
            r = os.popen("docker logs --tail=10 datacenter_sync_1")
            lines = r.readlines()
            if len(lines) > 0:
                line = lines[-1]
            if " Scanning events from blocks " in line:
                block = line.split(" ")[-1]
            elif "Current block: " in line:
                block = line.split(" ")[2]
            if block != "0":
                block = block.replace("\x1b[0m\n", "")
                self.info['last_sync_block'] = block
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
            Last sync block: {self.info['last_sync_block']}
            -----------------------------------------------
            Logs size: {self.info['logs']}
            -----------------------------------------------
            Disk: {self.info['disk']}
            CPU: {self.info['cpu']}
            Memory: {self.info['memory']}
            -----------------------------------------------
            Sync service: {true if self.info['sync'] else false}
            GRPC service: {true if self.info['grpc'] else false}
            Restful service: {true if self.info['restful'] else false}
            Mongo service: {true if self.info['mongo'] else false}
            Graphql service: {true if self.info['graphql'] else false}
            """
            self.discord_bot.push_message(msg)
            await asyncio.sleep(self.config['check_interval'])

    def get_tasks(self, loop: asyncio.AbstractEventLoop):
        return [loop.create_task(self.read_info())]

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self.get_tasks(loop)))
        loop.close()