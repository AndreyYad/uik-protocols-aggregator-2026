from fontTools.varLib.instancer import names

from uik_info.candidates import Candidates
from uik_info.candidate import Candidate
from uik_info.uik import Uik

class Uiks():
    def __init__(self, list_uiks_data: list[dict]):
        self.list_uiks: list[Uik] = []
        self.candidate_full: dict[str, list[int]] = {}
        count = 0

        for uik_data in list_uiks_data:
            self.list_uiks.append(Uik(uik_data))

        self.sortCandidates()

        for candidate_uik_info in [
            candidate
            for uik in self.list_uiks
            for candidate in uik.getCandidates().getCandidateList()
        ]:
            count += 1
            name = candidate_uik_info.getName()
            if name not in self.candidate_full:
                self.candidate_full[name] = []
            self.candidate_full[name].append(candidate_uik_info.getVotes())

        for name in self.candidate_full.keys():
            self.candidate_full[name] = sum(self.candidate_full[name])

    def sortCandidates(self):
        sorted_names = self.getSortsNames()

        order = {name: i for i, name in enumerate(sorted_names)}

        for uik in self.list_uiks:
            candidates = uik.getCandidates().getCandidateList()

            candidates.sort(
                key=lambda candidate: order.get(candidate.getName(), len(order))
            )

    def getListUiks(self) -> list[Uik]:
        return self.list_uiks

    def getSortsNames(self) -> list[str]:
        names = sorted(self.candidate_full, key=self.candidate_full.get, reverse=True)
        return names