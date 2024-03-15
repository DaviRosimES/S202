from database import Database
from pokedex import Pokedex

def main():
    db = Database(database="pokedex", collection="pokemons")
    db.resetDatabase()  # Se precisar resetar o banco de dados

    pokedex = Pokedex(db)

    # Chamando cada uma das funções da Pokedex
    pokedex.pokemonsWithSameType(["Grass"])
    pokedex.pokemonsWithWeaknesses(["Fire"])
    pokedex.pokemonsWithTallerHeight(1.5)
    pokedex.pokemonsEvolution()
    pokedex.pokemonsWithNextEvolution()

if __name__ == "__main__":
    main()
