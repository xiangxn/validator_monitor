import sys

sys.path.append('./validator_monitor/grpc')
import grpc
from validator_monitor.grpc.nutbox_bot_pb2_grpc import NutboxBotStub
from validator_monitor.grpc.nutbox_bot_pb2 import PushMessageRequest, BaseReply


class TestGRPC(object):

    def test_grpc_client(self):
        with grpc.insecure_channel("127.0.0.1:10086") as channel:
            client = NutboxBotStub(channel)
            res: BaseReply = client.PushMessage(PushMessageRequest(channel="service-monitoring", message="Nutbox monitors bot test messages"))
            assert res.code == 0
