from database import Database
from game import GameDAO


"""
Cria uma instância da classe Database para estabelecer
uma conexão com o banco de dados Neo4j
"""
db = Database(
    "bolt://44.200.159.206:7687",
    "neo4j",
    "procedure-thoughts-waters")
db.drop_all()

# Cria uma instância do GameDAO passando a instância do banco de dados
game_dao = GameDAO(db)

# Criação de um jogador
player_creation_result = game_dao.create_player("Alice")
print("Player criado:", player_creation_result)

# Atualização do nome de um jogador
player_update_result = game_dao.update_player(player_id=1, new_name="Bob")
print("Nome do jogador atualizado:", player_update_result)

# Exclusão de um jogador
player_deletion_result = game_dao.delete_player(player_id=1)
print("Player excluído:", player_deletion_result)

# Criação de uma partida com dois jogadores
match_creation_result = game_dao.create_match(
    ["Alice", "Bob"],
    result="Empate")
print("Partida criada:", match_creation_result)

# Obtenção da lista de jogadores
players_list = game_dao.get_players()
print("Lista de jogadores:", players_list)

# Obtenção de uma partida específica pelo seu identificador
match_info = game_dao.get_match(match_id=1)
print("Informações da partida:", match_info)

# Obtenção do histórico de partidas de um jogador específico pelo seu id
player_matches = game_dao.get_player_matches(player_id=1)
print("Histórico de partidas do jogador:", player_matches)

# Fechando a conexão com o banco de dados
db.close()
