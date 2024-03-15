from database import Database
from writeAJson import writeAJson

class Pokedex:
    def __init__(self, database: Database):
        self.db = database

    def pokemonsWithSameType(self, types):
        pokemons = self.db.collection.find({"type": {"$in": types}})
        writeAJson(pokemons, "PokemonsDoMesmoTipo")

    def pokemonsWithWeaknesses(self, weaknesses):
        pokemons = self.db.collection.find({"weaknesses": {"$in" : weaknesses}})
        writeAJson(pokemons, "PokemonsComFraqueza")

    def pokemonsWithTallerHeight(self, height):
        pokemons = self.db.collection.find()
        filtered_pokemons = [pokemon for pokemon in pokemons if float(''.join(filter(str.isdigit, pokemon['height']))) > height]
        writeAJson(filtered_pokemons, "PokemonsComAlturaMaior")

    def pokemonsEvolution(self):
        pokemons = self.db.collection.find({"next_evolution": {"$exists": True}})
        writeAJson(pokemons, "EvolucoesDePokemons")

    def pokemonsWithNextEvolution(self):
        pokemons = self.db.collection.find({"next_evolution": {"$exists": True}})
        writeAJson(pokemons, "PokemonsComEvolucao")
