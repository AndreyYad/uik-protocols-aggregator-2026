from typing import cast

LABELS = (
    "Число избирателей, внесенных в список избирателей на момент окончания голосования",
    "Число избирательных бюллетеней, полученных участковой избирательной комиссией",
    "Число избирательных бюллетеней, выданных избирателям, проголосовавшим досрочно",
    "Число избирательных бюллетеней, выданных участковой избирательной комиссией избирателям в помещении для голосования в день голосования",
    "Число избирательных бюллетеней, выданных избирателям, проголосовавшим вне помещения для голосования в день голосования",
    "Число погашенных избирательных бюллетеней",
    "Число избирательных бюллетеней, содержащихся в переносных ящиках для голосования",
    "Число избирательных бюллетеней, содержащихся в стационарных ящиках для голосования",
    "Число недействительных избирательных бюллетеней",
    "Число действительных избирательных бюллетеней",
    "Число утраченных избирательных бюллетеней",
    "Число избирательных бюллетеней, не учтенных при получении",
    "Явка, %"
)

class Protocol:
    PROTOCOL_LENGTH = 13

    COUNT_VOTERS_INDEX = 0
    COUNT_INVALID_INDEX = 8
    COUNT_VALID_INDEX = 9
    TURNOUT_INDEX = 12

    def __init__(self, protocol:list[int | float]):
        if len(protocol) not in (
            self.PROTOCOL_LENGTH - 1,
            self.PROTOCOL_LENGTH
        ):
            raise ValueError(
                f"Протокол должен содержать "
                f"{self.PROTOCOL_LENGTH - 1} (без явки) "
                f"или {self.PROTOCOL_LENGTH} "
                f"(уже с явкой) значений"
            )

        if len(protocol) == self.PROTOCOL_LENGTH and not (
                0 <= protocol[self.TURNOUT_INDEX] <= 1
        ):
            raise ValueError(
                f"Процент явки должен находиться "
                f"в диапазоне от 0 до 1"
            )

        self.protocol = protocol.copy()
        if len(protocol) != self.PROTOCOL_LENGTH:
            self.protocol.append(self._calculate_turnout())

    def get_data(self) -> list[int | float]:
        return self.protocol.copy()

    def _calculate_turnout(self) -> float:
        try:
            return round(
                (
                    self.protocol[self.COUNT_INVALID_INDEX] +
                    self.protocol[self.COUNT_VALID_INDEX]
                ) / self.protocol[self.COUNT_VOTERS_INDEX],
                3
            )
        except ZeroDivisionError:
            return 0

    @classmethod
    def sum(cls, protocols: list["Protocol"]) -> "Protocol":
        if not protocols:
            raise ValueError("Нельзя суммировать пустой список протоколов")

        protocols_data = [
            protocol.get_data()[:cls.TURNOUT_INDEX]
            for protocol in protocols
        ]

        sum_protocol = [
            cast(int | float, sum(data))
            for data in zip(*protocols_data)
        ]

        return cls(sum_protocol)
