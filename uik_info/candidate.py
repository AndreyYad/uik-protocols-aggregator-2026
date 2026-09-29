from typing import Any


class Candidate:

    def __init__(self, name: str = "", party: str = "", party_name: str = "", votes: int = 0, percent: float| None = None):
        self.name: str = name
        self.party: str = party
        self.party_name: str = party_name
        self.votes: int = votes
        self.percent: float | None = percent

    @classmethod
    def from_dict(cls, candidate_data: dict[str, Any]) -> "Candidate":
        return cls(
            name=candidate_data["name"],
            party=candidate_data["key"],
            party_name=candidate_data["party"],
            votes=candidate_data["votes"]
        )

    def get_name(self) -> str:
        if self.party_name:
            name = f"{self.name}\n\n{self.party_name}"
        else:
            name = self.name
        return name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_party(self) -> str:
        return self.party

    def set_party(self, party: str) -> None:
        self.party = party

    def get_party_name(self) -> str:
        return self.party

    def set_party_name(self, party_name: str) -> None:
        self.party_name = party_name

    def get_votes(self) -> int:
        return self.votes

    def set_votes(self, votes: int) -> None:
        self.votes = votes

    def get_percent(self) -> float | None:
        return self.percent

    def set_percent(self, percent: float) -> None:
        self.percent = percent