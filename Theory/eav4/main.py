from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

# Carregando informações de autenticação
with open("eav4-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

# Configurando o acesso ao banco de dados Cassandra
cloud_config = {
    'secure_connect_bundle': 'secure-connect-eav4.zip'
}

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

session.set_keyspace('eav4')


def consultar_peca(nome_peca):
    # Consulta para obter informações sobre a peça fornecido
    consulta = session.prepare(
        '''SELECT id,nome, carro, estante, nivel, quantidade
        FROM peca WHERE nome = ?
        ALLOW FILTERING''')
    resultado = session.execute(consulta, [nome_peca])

    # Verificando se a peça foi encontrado
    if resultado:
        for linha in resultado:
            print("Id:", linha.id)
            print("Nome:", linha.nome)
            print("Carro:", linha.carro)
            print("Estante:", linha.estante)
            print("Nível:", linha.nivel)
            print("Quantidade:", linha.quantidade)
    else:
        print("Carro não encontrado.")


# Solicitando o nome do carro ao usuário
nome_peca = input("Digite o nome da peça que deseja consultar: ")

# Chamando a função para consultar o carro
consultar_peca(nome_peca)

# Fechando a conexão com o cluster
cluster.shutdown()
