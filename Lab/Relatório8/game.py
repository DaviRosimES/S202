class GameDAO:
    def __init__(self, database):
        self.db = database

    def create_player(self, player_name):
        query = """
        CREATE (p:Player {name: $name}) RETURN p
        """
        return self.db.execute_query(
            query,
            {"name": player_name}
        )

    def update_player(self, player_id, new_name):
        query = """
        MATCH (p:Player) WHERE id(p) = $player_id
        SET p.name = $new_name
        """
        return self.db.execute_query(
            query,
            {"player_id": player_id,
             "new_name": new_name}
        )

    def delete_player(self, player_id):
        query = """
        MATCH (p:Player) WHERE id(p) = $player_id DETACH DELETE p
        """
        return self.db.execute_query(
            query,
            {"player_id": player_id}
        )

    def create_match(self, players, result):
        players_query = ", ".join(
            [f"(p{id}:Player)" for id in range(len(players))]
        )
        query = f"""
        CREATE ({players_query})-[:PLAYED_IN]->(m:Match {{result: $result}})
        RETURN m
        """
        return self.db.execute_query(
            query,
            {"result": result}
        )

    def get_players(self):
        query = """
        MATCH (p:Player) RETURN p
        """
        return self.db.execute_query(query)

    def get_match(self, match_id):
        query = "MATCH (m:Match) WHERE id(m) = $match_id RETURN m"
        return self.db.execute_query(
            query,
            {"match_id": match_id}
        )

    def get_player_matches(self, player_id):
        query = """
        MATCH (p:Player)-[:PLAYED_IN]->(m:Match) WHERE id(p) = $player_id
        RETURN m
        """
        return self.db.execute_query(
            query,
            {"player_id": player_id}
        )
