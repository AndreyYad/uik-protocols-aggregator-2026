from typing import Any

from pip._internal.resolution.resolvelib import candidates

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

    def __init__(self, list_candidates_data: list):
        self.list_candidates: list[Candidate] = []
        for candidate_data in list_candidates_data:
            self.list_candidates.append(Candidate(candidate_data))

        all_votes = 0;
        for candidate in self.list_candidates:
            all_votes += candidate.votes

        for candidate in self.list_candidates:
            try:
                candidate.setPercent(round(candidate.votes/all_votes, 2))
            except ZeroDivisionError:
                candidate.setPercent(0)

    @staticmethod
    def getCandidatesByParties(votes: list[int]) -> list[dict[str, Any]]:
        candidates = []
        for i, party_info in enumerate(PARTIES):
            party_data = {
                "name": party_info[0],
                "key": party_info[1],
                "party": None,
                "votes": votes[i]
            }
            candidates.append(party_data)
        return candidates

    def getCandidateList(self) -> list[Candidate]:
        return self.list_candidates