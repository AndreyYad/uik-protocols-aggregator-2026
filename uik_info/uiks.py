from fontTools.varLib.instancer import names

from uik_info.candidates import Candidates
from uik_info.candidate import Candidate
from uik_info.uik import Uik
from uik_info.sum_protocol import SumProtocol

class Uiks():
    def __init__(self, list_uiks_data: list[dict] | None):
        if list_uiks_data is None:
            return

        self.list_uiks: list[Uik] = []
        self.sum_protocol: SumProtocol
        self.candidate_full: dict[str, list[int]] = {}
        count = 0

        for uik_data in list_uiks_data:
            self.list_uiks.append(Uik(uik_data))

        self.sum_protocol = SumProtocol([uik.get_protocol() for uik in self.list_uiks])

        for candidate_uik_info in [
            candidate
            for uik in self.list_uiks
            for candidate in uik.get_candidates().get_candidate_list()
        ]:
            count += 1
            name = candidate_uik_info.get_name()
            if name not in self.candidate_full:
                self.candidate_full[name] = []
            self.candidate_full[name].append(candidate_uik_info.get_votes())

        for name in self.candidate_full.keys():
            self.candidate_full[name] = sum(self.candidate_full[name])

        self.sort_candidates()

    def sort_candidates(self):
        sorted_names = self.get_sorts_names()

        order = {name: i for i, name in enumerate(sorted_names)}

        for uik in self.list_uiks:
            candidates = uik.get_candidates().get_candidate_list()

            candidates.sort(
                key=lambda candidate: order.get(candidate.get_name(), len(order))
            )

    def get_list_uiks(self) -> list[Uik]:
        return self.list_uiks

    def get_sum_protocol(self) -> SumProtocol:
        return self.sum_protocol

    def get_sum_all_votes(self) -> int:
        return sum(list(self.get_candidates_full().values()))

    def get_candidates_full(self) -> dict[str, int]:
        return self.candidate_full

    def get_sorts_names(self) -> list[str]:
        names = sorted(self.candidate_full, key=self.candidate_full.get, reverse=True)
        return names