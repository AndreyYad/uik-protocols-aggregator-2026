from .protocol import Protocol
class SumProtocol(Protocol):
    list_protocols = None

    def __init__(self, list_protocols: list(Protocol)):
        self.list_protocols = list_protocols
        super().__init__([
            sum(columns)
            for columns in zip(*[p.protocol for p in list_protocols])
        ])