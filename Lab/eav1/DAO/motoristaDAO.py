class MotoristaDAO:
    def __init__(self, database):
        self.db = database

    def create_motorista(self, nome, idade, cnh, corrida_):
        motorista = {"nome": nome, "idade": idade, "cnh": cnh, "corridas": []}
        try:
            self.db.collection.insert_one(motorista)
            print("Motorista criado com sucesso!")
        except Exception as e:
            print("Erro ao criar motorista:", e)

    def read_motorista(self, filtro=None):
        try:
            if filtro:
                motorista = self.db.collection.find_one(filtro)
                return motorista
            else:
                motoristas = list(self.db.collection.find())
                return motoristas
        except Exception as e:
            print("Erro ao ler motorista(s):", e)

    def update_motorista(self, filtro, novos_dados):
        try:
            self.db.collection.update_one(filtro, {"$set": novos_dados})
            print("Motorista atualizado com sucesso!")
        except Exception as e:
            print("Erro ao atualizar motorista:", e)

    def delete_motorista(self, filtro):
        try:
            self.db.collection.delete_one(filtro)
            print("Motorista deletado com sucesso!")
        except Exception as e:
            print("Erro ao deletar motorista:", e)

    def adicionar_corrida(self, motorista_id, corrida):
        try:
            self.db.collection.update_one(
                {"_id": motorista_id},
                {"$push": {"corridas": corrida}})
            print("Corrida adicionada ao motorista com sucesso!")
        except Exception as e:
            print("Erro ao adicionar corrida ao motorista:", e)

    def remover_corrida(self, motorista_id, corrida_id):
        try:
            self.db.collection.update_one(
                {"_id": motorista_id},
                {"$pull": {"corridas": {"_id": corrida_id}}})
            print("Corrida removida do motorista com sucesso!")
        except Exception as e:
            print("Erro ao remover corrida do motorista:", e)

    def atualizar_corrida(self, motorista_id, corrida_id, novos_dados):
        try:
            self.db.collection.update_one(
                {"_id": motorista_id, "corridas._id": corrida_id},
                {"$set": {"corridas.$": novos_dados}}
            )
            print("Corrida atualizada com sucesso!")
        except Exception as e:
            print("Erro ao atualizar corrida:", e)

    def ler_corridas_motorista(self, motorista_id):
        try:
            motorista = self.db.collection.find_one({"_id": motorista_id})
            corridas = motorista.get("corridas", [])
            return corridas
        except Exception as e:
            print("Erro ao ler corridas do motorista:", e)
