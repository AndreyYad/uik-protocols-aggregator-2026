class Candidate:

    def __init__(self, candidate_data: dict):
        self.name: str = candidate_data["name"] + '\n' + candidate_data["party"]
        self.party: str = candidate_data["key"]
        self.votes: int = candidate_data["votes"]
        self.percent: float = candidate_data["percent"]

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