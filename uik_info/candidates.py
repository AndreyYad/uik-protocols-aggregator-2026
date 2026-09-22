from uik_info.candidate import Candidate

class Candidates:
    list_candidates: list[Candidate] = []

    def __init__(self, list_candidates_data: list):
        for candidate_data in list_candidates_data:
            self.list_candidate.append(Candidate(candidate_data))