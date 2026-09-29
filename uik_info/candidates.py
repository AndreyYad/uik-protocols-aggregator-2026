from typing import Any

from uik_info.candidate import Candidate

PARTIES = [
    ["ВСЕРОССИЙСКАЯ ПОЛИТИЧЕСКАЯ ПАРТИЯ \"РОДИНА\"", "other"],
    ["Всероссийская политическая партия \"ЕДИНАЯ РОССИЯ\"", "er"],
    ["КПРФ - политическая партия КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ", "kprf"],
    ["ПАРТИЯ ПЕНСИОНЕРОВ", "other"],
    ["Политическая партия \"НОВЫЕ ЛЮДИ\"", "np"],
    ["Политическая партия \"Партия прямой демократии\"", "other"],
    ["Политическая партия \"Российская экологическая партия \"ЗЕЛЁНЫЕ\"", "other"],
    ["Политическая партия КОММУНИСТИЧЕСКАЯ ПАРТИЯ КОММУНИСТЫ РОССИИ", "other"],
    ["Политическая партия ЛДПР – Либерально-демократическая партия России", "ldpr"],
    ["Социалистическая политическая партия СПРАВЕДЛИВАЯ РОССИЯ", "sr"]
]

class Candidates:

    def __init__(self, list_candidates: list[Candidate]):
        self.list_candidates: list[Candidate] = list_candidates

        all_votes = 0
        for candidate in self.list_candidates:
            all_votes += candidate.votes

        for candidate in self.list_candidates:
            try:
                candidate.set_percent(round(candidate.votes/all_votes, 4))
            except ZeroDivisionError:
                candidate.set_percent(0)

    @classmethod
    def from_dict(cls, candidates_data: list[dict[str, Any]]):
        list_candidates: list[Candidate] = []
        for candidate_data in candidates_data:
            list_candidates.append(Candidate.from_dict(candidate_data))
        return Candidates(list_candidates)

    @classmethod
    def from_parties(cls, votes: list[int]):
        candidates_party: list[Candidate] = []
        for party_info_index, party_info in enumerate(PARTIES):
            candidates_party.append(
                Candidate(
                    name=party_info[0],
                    party=party_info[1],
                    party_name="",
                    votes=votes[party_info_index]
                )
            )
        return Candidates(candidates_party)

    def get_candidate_list(self) -> list[Candidate]:
        return self.list_candidates