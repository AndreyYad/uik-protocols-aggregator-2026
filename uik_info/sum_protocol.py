from .protocol import Protocol
class SumProtocol(Protocol):
    def __init__(self, list_protocols: list[Protocol]):
        self.list_protocols = list_protocols

        sum_protocol = [
            sum(columns) if all(isinstance(x, (int, float)) for x in columns) else ""
            for columns in zip(*[p.protocol for p in list_protocols])
        ]

        sum_protocol[12] = round(sum_protocol[12] / len(list_protocols), 3)

        super().__init__(sum_protocol)