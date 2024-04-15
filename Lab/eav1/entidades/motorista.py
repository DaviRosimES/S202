from corrida import Corrida


class Motorista:
    def __init__(self, nota, corridas: Corrida) -> None:
        self.nota = nota
        self.corridas = corridas
