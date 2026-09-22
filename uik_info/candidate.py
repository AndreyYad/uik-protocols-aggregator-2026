class Candidate:
    name: str = None
    party: str = None
    votes: int = None

    def __init__(self, candidate_data: dict):
        self.name = candidate_data["name"] + '\n' + candidate_data["party"]
        self.party = candidate_data["key"]
        self.votes = candidate_data["votes"]

    def getName(self) -> str:
        return self.name

    def getParty(self) -> str:
        return self.party

    def getVotes(self) -> int:
        return self.votes