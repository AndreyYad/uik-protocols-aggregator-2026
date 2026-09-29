from uik_info.protocol import Protocol
from uik_info.candidates import Candidates

class Uik:

    def __init__(self, uik_data: dict):
        id: int = None
        tik: str = None
        protocol: Protocol = None
        candidates: Candidates = None

        self.id = uik_data["num"]
        self.tik = uik_data["tik"]
        self.protocol = Protocol(uik_data["protocol"])
        try:
            self.candidates = Candidates(uik_data["candidates"])
        except KeyError:
            candidatesByParties = Candidates.get_candidates_by_parties(uik_data["votes"])
            self.candidates = Candidates(candidatesByParties)

    def get_id(self) -> int:
        return self.id

    def get_tik(self) -> str:
        return self.tik

    def get_protocol(self) -> Protocol:
        return self.protocol

    def get_candidates(self) -> Candidates:
        return self.candidates