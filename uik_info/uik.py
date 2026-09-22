from uik_info.protocol import Protocol
from uik_info.candidates import Candidates

class UikInfo:
    id: int = None
    tik: str = None
    protocol: Protocol = None
    candidates: Candidates = None

    def __init__(self, uik_data: dict):
        self.id = uik_data["num"]
        self.tik = uik_data["tik"]
        self.protocol = Protocol(uik_data["protocol"])
        self.candidates = Candidates(uik_data["candidates"])

    def getId(self) -> int:
        return self.id

    def getTik(self) -> str:
        return self.tik

    def getProtocol(self) -> Protocol:
        return self.protocol

    def getCandidates(self) -> Candidates:
        return self.candidates