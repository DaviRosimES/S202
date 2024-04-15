class CorridaDAO:
    def __init__(self, database):
        self.db = database

    def create_corrida(self, nota, distancia, valor, passageiro):
        corrida = {
            "nota": nota,
            "distancia": distancia,
            "valor": valor,
            "passageiro": passageiro}
        try:
            self.db.collection.insert_one(corrida)
            print("Corrida criada com sucesso!")
            return corrida["_id"]
        except Exception as e:
            print("Erro ao criar corrida:", e)

    def read_corrida(self, corrida_id):
        try:
            corrida = self.db.collection.find_one({"_id": corrida_id})
            return corrida
        except Exception as e:
            print("Erro ao ler corrida:", e)

    def update_corrida(self, corrida_id, novos_dados):
        try:
            self.db.collection.update_one(
                {"_id": corrida_id},
                {"$set": novos_dados})
            print("Corrida atualizada com sucesso!")
        except Exception as e:
            print("Erro ao atualizar corrida:", e)

    def delete_corrida(self, corrida_id):
        try:
            self.db.collection.delete_one({"_id": corrida_id})
            print("Corrida deletada com sucesso!")
        except Exception as e:
            print("Erro ao deletar corrida:", e)
