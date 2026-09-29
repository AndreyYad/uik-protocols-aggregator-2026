class Candidate:

    def __init__(self, candidate_data: dict):
        self.percent = None
        self.name: str = candidate_data["name"]
        self.party: str = candidate_data["key"]
        self.votes: int = candidate_data["votes"]
        self.percent: float

        name_party = candidate_data["party"]
        if name_party is not None:
            self.name += '\n\n' + name_party

    def get_name(self) -> str:
        return self.name

    def get_party(self) -> str:
        return self.party

    def get_votes(self) -> int:
        return self.votes

    def get_percent(self) -> float:
        return self.percent

    def set_percent(self, percent: float) -> None:
        self.percent = percent