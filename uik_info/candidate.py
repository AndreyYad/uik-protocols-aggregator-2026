class Candidate:

    def __init__(self, candidate_data: dict):
        self.name: str = candidate_data["name"]
        self.party: str = candidate_data["key"]
        self.votes: int = candidate_data["votes"]
        self.percent: float

        name_party = candidate_data["party"]
        if name_party is not None:
            self.name += '\n\n' + name_party

    def getName(self) -> str:
        return self.name

    def getParty(self) -> str:
        return self.party

    def getVotes(self) -> int:
        return self.votes

    def getPercent(self) -> float:
        return self.percent

    def setPercent(self, percent: float) -> None:
        self.percent = percent