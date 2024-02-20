class Professor:
    def __init__(self, nome):
        self.nome = nome

    def ministrar_aula(self, assunto):
        print(f"\nO professor {self.nome} está ministrando uma aula sobre {assunto}")