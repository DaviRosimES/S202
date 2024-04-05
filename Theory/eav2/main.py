from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

uri = "neo4j+s://f9c1d5fa.databases.neo4j.io"
user = "neo4j"
password = "SqR3PCyL4ER5hqJmXMj04_AjnhLqnCxdOnGYZbUF-rM"

driver = GraphDatabase.driver(uri, auth=(user, password))


def get_economist_in_the_family(tx):
    """
        Função para retornar o(s) ecnomista(s) da familia.
    """
    query = """
        MATCH (n:Economista)
        RETURN n;
    """
    try:
        result = tx.run(query)
        return [{'economista': row['n']} for row in result]

    except ServiceUnavailable as exception:
        print("{query} raised an error: \n {exception}".format(
            query=query,
            exception=exception))
        raise


def get_whose_father(tx, father):
    """
        Função para retornar quem são os filhos do parametro father.
    """
    query = """
        MATCH (father:Pessoa {nome: $father})-[:PAI_DE]->(filho)
        RETURN filho.nome AS nome_filho;
    """
    try:
        result = tx.run(query, father=father)
        return [{'nome_filho': row['nome_filho']} for row in result]

    except ServiceUnavailable as exception:
        print("{query} raised an error: \n {exception}".format(
            query=query,
            exception=exception))
        raise


def get_date_since(tx, p1, p2):
    """
        Função para retornar desde quando alguem namora com outro alguem.
    """
    query = """
        MATCH(:Pessoa {nome: $p1})-[r:NAMORADO_DE]->(:Pessoa {nome: $p2})
        RETURN r.desde as date_since
    """
    try:
        result = tx.run(query, p1=p1, p2=p2)
        return [{'date_since': row['date_since']} for row in result]

    except ServiceUnavailable as exception:
        print("{query} raised an error: \n {exception}".format(
            query=query,
            exception=exception))
        raise


with driver.session() as session:
    result = session.execute_read(get_economist_in_the_family)
    print("Economistas na família:")
    for record in result:
        print("- Nome:", record['economista']['nome'])
        print("  Idade:", record['economista']['idade'])
        print("  Sexo:", record['economista']['sexo'])

print()

with driver.session() as session:
    result = session.execute_read(get_date_since, "Davi Rosim", "Ana Clara")
    print("Data em que Davi Rosim começou a namorar Ana Clara:")
    for record in result:
        print("- Desde:", record['date_since'])

print()

with driver.session() as session:
    result = session.execute_read(get_whose_father, "José")
    print("Filhos de José:")
    for record in result:
        print("-", record['nome_filho'])


driver.close()
