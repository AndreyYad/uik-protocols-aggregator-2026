from uik_info.protocol import Protocol
from uik_info.candidates import Candidates

class Uik:

    def __init__(self, uik_data: dict):
        self.id: int = uik_data["num"]
        self.tik: str = uik_data["tik"]
        self.protocol: Protocol = Protocol(uik_data["protocol"])
        try:
            self.candidates: Candidates = Candidates.from_dict(uik_data["candidates"])
        except KeyError:
            self.candidates: Candidates = Candidates.from_parties(uik_data["votes"])

    def get_id(self) -> int:
        return self.id

    def get_tik(self) -> str:
        return self.tik

    def get_protocol(self) -> Protocol:
        return self.protocol

    def get_candidates(self) -> Candidates:
        return self.candidates