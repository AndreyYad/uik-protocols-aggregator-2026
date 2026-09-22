from uik_info.candidate import Candidate

class Candidates:

    def __init__(self, list_candidates_data: list):
        self.list_candidates: list[Candidate] = []
        for candidate_data in list_candidates_data:
            self.list_candidates.append(Candidate(candidate_data))

        all_votes = 0;
        for candidate in self.list_candidates:
            all_votes += candidate.votes

        for candidate in self.list_candidates:
            candidate.setPercent(round(candidate.votes/all_votes))

    def getCandidateList(self) -> list[Candidate]:
        return self.list_candidates