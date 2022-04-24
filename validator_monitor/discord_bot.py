import grpc
from validator_monitor.grpc.nutbox_bot_pb2_grpc import NutboxBotStub
from validator_monitor.grpc.nutbox_bot_pb2 import PushMessageRequest


class DiscordBot:

    def __init__(self, config, logger) -> None:
        self.config = config
        self.logger = logger

    def push_message(self, msg: str, channel: str = None):
        if not channel:
            channel = self.config['channels']['monitor']
        with grpc.insecure_channel(self.config['bot_server']) as grpc_channel:
            client = NutboxBotStub(grpc_channel)
            pr = PushMessageRequest(channel=channel, message=msg)
            res = client.PushMessage(pr)
            if res.code != 0:
                self.logger.error(f"push_message error: {res.msg}")