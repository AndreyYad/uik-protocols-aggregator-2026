from .protocol import Protocol
class SumProtocol(Protocol):
    def __init__(self, list_protocols: list(Protocol)):
        self.list_protocols = list_protocols
        super().__init__([
            sum(columns) if all(isinstance(x, (int, float)) for x in columns) else ""
            for columns in zip(*[p.protocol for p in list_protocols])
        ])