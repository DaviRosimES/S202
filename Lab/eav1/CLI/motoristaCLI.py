from DAO.motoristaDAO import MotoristaDAO
from DAO.passageiroDAO import PassageiroDAO
from DAO.corridaDAO import CorridaDAO
from CLI.simpleCLI import SimpleCLI


class MotoristaCLI(SimpleCLI):
    def __init__(self, motorista_dao: MotoristaDAO,
                 passageiro_dao: PassageiroDAO,
                 corrida_dao: CorridaDAO):
        super().__init__()
        self.motorista_dao = motorista_dao
        self.passageiro_dao = passageiro_dao
        self.corrida_dao = corrida_dao
        self.add_command("create", self.create_motorista)
        self.add_command("read", self.read_motorista)
        self.add_command("update", self.update_motorista)
        self.add_command("delete", self.delete_motorista)

    def create_motorista(self):
        nome = input("Digite o nome do motorista: ")
        idade = int(input("Digite a idade do motorista: "))
        cnh = input("Digite a CNH do motorista: ")

        # Criar passageiro associado ao motorista
        nome_passageiro = input("Digite o nome do passageiro: ")
        documento_passageiro = input("Digite o documento do passageiro: ")
        passageiro_id = self.passageiro_dao.create_passageiro(
            nome_passageiro,
            documento_passageiro)

        # Criar corrida associada ao motorista
        nota_corrida = float(input("Digite a nota da corrida: "))
        distancia_corrida = float(input("Digite a distância da corrida: "))
        valor_corrida = float(input("Digite o valor da corrida: "))
        corrida_id = self.corrida_dao.create_corrida(
            nota_corrida,
            distancia_corrida,
            valor_corrida,
            passageiro_id)

        # Criar motorista
        self.motorista_dao.create_motorista(nome, idade, cnh, corrida_id)

        print("Motorista criado com sucesso.")

    def read_motorista(self):
        filtro = input("Digite o filtro (deixe em branco para todos): ")
        motorista = self.motorista_dao.read_motorista(filtro)
        if motorista:
            print(motorista)
        else:
            print("Motorista não encontrado.")

    def update_motorista(self):
        filtro = input("Digite o filtro para identificar o motorista a ser atualizado: ")
        novos_dados = {}
        nome = input("Digite o novo nome (deixe em branco para manter o atual): ")
        idade = input("Digite a nova idade (deixe em branco para manter a atual): ")
        cnh = input("Digite a nova CNH (deixe em branco para manter a atual): ")
        if nome:
            novos_dados["nome"] = nome
        if idade:
            novos_dados["idade"] = int(idade)
        if cnh:
            novos_dados["cnh"] = cnh
        if novos_dados:
            self.motorista_dao.update_motorista(filtro, novos_dados)
        else:
            print("Nenhuma atualização fornecida.")

    def delete_motorista(self):
        filtro = input("Digite o filtro para identificar o motorista a ser excluído: ")
        self.motorista_dao.delete_motorista(filtro)

    def run(self):
        print("Bem-vindo ao CLI do motorista!")
        print("Comandos disponíveis: create, read, update, delete, quit")
        super().run()
