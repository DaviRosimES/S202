from passageiro import Passageiro


class Corrida:
    def __init__(self, nota, distancia, valor, passageiro: Passageiro) -> None:
        self.nota = nota
        self.distancia = distancia
        self.valor = valor
        self.passageiro = passageiro
