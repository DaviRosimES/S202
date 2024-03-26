from database import Database
from livroModel import LivroModel


def main():
    db = Database(database="relatorio5", collection="livros")
    livroModel = LivroModel(database=db)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            titulo = input("Digite o titulo do livro: ")
            autor = input("Digite o nome do autor: ")
            ano = int(input("Digite o ano em que o livro foi lançado: "))
            preco = float(input("Digite o preço do livro: "))
            livroModel.create_book(titulo, autor, ano, preco)
        elif opcao == "2":
            id = input("Digite o id do livro desejado: ")
            livroModel.read_book_by_id(id)
        elif opcao == "3":
            id = input("Digite o id do livro desejado: ")
            titulo = input("Digite o titulo do livro: ")
            autor = input("Digite o nome do autor: ")
            ano = int(input("Digite o ano em que o livro foi lançado: "))
            preco = float(input("Digite o preço do livro: "))
            livroModel.update_book(id, titulo, autor, ano, preco)
        elif opcao == "4":
            id = input("Digite o id do livro desejado: ")
            livroModel.delete_book(id)
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


def exibir_menu():
    print("===== Menu =====")
    print("1. Criar livro")
    print("2. Listar livros")
    print("3. Atualizar livro")
    print("4. Deletar livro")
    print("5. Sair")


if __name__ == "__main__":
    main()