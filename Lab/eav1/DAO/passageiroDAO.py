class PassageiroDAO:
    def __init__(self, database):
        self.db = database

    def create_passageiro(self, nome, documento):
        passageiro = {"nome": nome, "documento": documento}
        try:
            self.db.collection.insert_one(passageiro)
            print("Passageiro criado com sucesso!")
            return passageiro["_id"]
        except Exception as e:
            print("Erro ao criar passageiro:", e)

    def read_passageiro(self, passageiro_id):
        try:
            passageiro = self.db.collection.find_one({"_id": passageiro_id})
            return passageiro
        except Exception as e:
            print("Erro ao ler passageiro:", e)

    def update_passageiro(self, passageiro_id, novos_dados):
        try:
            self.db.collection.update_one(
                {"_id": passageiro_id},
                {"$set": novos_dados})
            print("Passageiro atualizado com sucesso!")
        except Exception as e:
            print("Erro ao atualizar passageiro:", e)

    def delete_passageiro(self, passageiro_id):
        try:
            self.db.collection.delete_one({"_id": passageiro_id})
            print("Passageiro deletado com sucesso!")
        except Exception as e:
            print("Erro ao deletar passageiro:", e)
