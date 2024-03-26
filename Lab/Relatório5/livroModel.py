from pymongo import MongoClient
from bson.objectid import ObjectId

class LivroModel: 
    def __init__(self, database):
        """
        Construtor da classe LivroModel.

        Args:
            database: Objeto de conexão com o banco de dados.
        """
        self.db = database

    def create_book(self, titulo:str, autor:str, ano: int, preco:float):
        """
        Cria um novo livro na coleção de livros.

        Args:
            titulo: Título do livro.
            autor: Autor do livro.
            ano: Ano de publicação do livro.
            preco: Preço do livro.

        Returns:
            str: O ID do livro criado no banco de dados.
        """
        try:
            res = self.db.collection.insert_one({"titulo": titulo, "autor" : autor, "ano": ano, "preco": preco})
            print(f"Book created with id: {res.inserted_id}")
            return res.inserted_id
        except Exception as e:
            print(f"An error occurred while creating person: {e}")
            return None

    def read_book_by_id(self, id: str):
        """
        Retorna as informações de um livro com base no ID fornecido.

        Args:
            id: O ID do livro a ser recuperado.

        Returns:
            dict: As informações do livro encontrado.
        """
        try:
            res = self.db.collection.find_one({"_id": ObjectId(id)})
            print(f"Book found: {res}")
            return res
        except Exception as e:
            print(f"An error occurred while reading person: {e}")
            return None

    def update_book(self, id:str, titulo:str, autor:str, ano: int, preco:float):
        """
        Atualiza as informações de um livro existente com base no ID fornecido.

        Args:
            id: O ID do livro a ser atualizado.
            titulo: Novo título do livro.
            autor: Novo autor do livro.
            ano: Novo ano de publicação do livro.
            preco: Novo preço do livro.

        Returns:
            int: O número de documentos modificados (deve ser 1 se a atualização for bem-sucedida).
        """
        try:
            res = self.db.collection.update_one({"_id": ObjectId(id)}, {"$set": {"titulo": titulo, "autor" : autor, "ano": ano, "preco": preco}})
            print(f"Book updated: {res.modified_count} document(s) modified")
            return res.modified_count
        except Exception as e:
            print(f"An error occurred while updating person: {e}")
            return None

    def delete_book(self, id:str):
        """
        Exclui um livro da coleção com base no ID fornecido.

        Args:
            id: O ID do livro a ser excluído.

        Returns:
            int: O número de documentos excluídos (deve ser 1 se a exclusão for bem-sucedida).
        """
        try:
            res = self.db.collection.delete_one({"_id": ObjectId(id)})
            print(f"Book deleted: {res.deleted_count} document(s) deleted")
            return res.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting person: {e}")
            return None