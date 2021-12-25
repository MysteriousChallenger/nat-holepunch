import time
from typing import Dict

from protocol.interface import (
    AbstractSerializableHandler,
    AbstractSerializableRequest,
    RequestData,
)

REQUEST_TYPE = "ping"


class PingRequest(AbstractSerializableRequest[float]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    TYPE = REQUEST_TYPE

    def prepare_payload(self):
        self.send_time = time.time()
        return {"send_time": self.send_time}

    def process_response(self, response: Dict) -> float:
        self.stop_time = time.time()
        reported_start_time = response["send_time"]
        recv_time = response["recv_time"]
        assert self.send_time == reported_start_time

        return self.stop_time - self.send_time


class PingRequestHandler(AbstractSerializableHandler):

    TYPE = REQUEST_TYPE

    def process_request(self, request: RequestData[Dict]) -> dict:
        recv_time = time.time()
        send_time = request.payload["send_time"]
        ping = recv_time - send_time
        response = {"send_time": send_time, "recv_time": recv_time}
        return response