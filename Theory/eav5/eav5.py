'''
Nessa atividade você deve usar seus conhecimentos sobre banco de dados chave-valor, mais especificamente sobre Redis para atender os requisitos pedidos.
Todos as questões tem um exemplo de caso de teste (com dados de entrada e saída esperada) para que você valide a sua solução.

Contexto: Imagine que você está desenvolvendo um banco de dados de cache para uma rede social. O objetivo do sistema é sempre exibir os posts mais recentes dessa rede social em ordem de interesse. 
Para isso, são mantidas informações sobre os interesses dos usuários e sobre o tópico de cada postagem.
Esse sistema deve armazenar o perfil de cada usuário, contendo o nome, o e-mail e um token de sessão. Além, disso o sistema deve manter uma lista de interesses para cada usuário, ordenando pelo score de interesse.
Por fim, o sistema deve manter informações sobre os posts, como id, conteúdo, e-mail do autor e data e hora de publicação. É registrado também uma lista de palavras chave sobre o post. Apenas as informações dos posts mais recentes devem ser mantidos no banco de dados (posts com mais de 5 horas devem ser excluídos). 
Considere que o interesse de um usuário por um post específico é a soma dos scores de cada interesse que está presente nas palavras chave desse post específico.

Questão 1)
Registe as informações dos seguintes usuários e realize a consutla para apresentar os dados.

Questão 2)
Registre uma lista de interesses para cada um dos usuários e realize a consutla para apresentar os dados.

Questão 3) 
Resgistre as informações sobre os posts mais recentes e realize a consutla para apresentar os dados.

Questão 4) 
Imagine que o usuário 3 acessa o seu feed. Realize uma consulta nos dados cadatrados par mostrar a lista dos posts mais interessantes para esse usuário.


Questão 5)
Imagine que será mantido também um lista de posts já vistos por um determinado usuário. Registre essa lista para cada um dos usuários e realize a consutla para apresentar os dados.

'''

import redis
from datetime import datetime, timedelta


# Conexão com o Redis
redis_conn = redis.Redis(
    host="seu_host", port=6379,  # Substitua "seu_host" e a porta pelo host e porta corretos
    username="default",
    password="sua_senha",  # Substitua "sua_senha" pela sua senha do Redis
    decode_responses=True
)


def questao_1(users):
    for user in users:
        user_key = f"user:{user['id']}"
        redis_conn.hmset(user_key, {"nome": user["nome"], "email": user["email"]})

    # Recuperando os dados para validação
    retrieved_users = []
    for user in users:
        user_key = f"user:{user['id']}"
        user_data = redis_conn.hgetall(user_key)
        user_data["id"] = user["id"]
        retrieved_users.append(user_data)

    return retrieved_users


def test_questao_1():
    users = [
        {"id":'1', "nome":"Serafim Amarantes", "email":"samarantes@g.com"},
        {"id":'2', "nome":"Tamara Borges", "email":"tam_borges@g.com"},
        {"id":'3', "nome":"Ubiratã Carvalho", "email":"bira@g.com"},
        {"id":'4', "nome":"Valéria Damasco", "email":"valeria_damasco@g.com"}
    ]

    assert users == sorted(questao_1(users), key=lambda d: d['id'])


def questao_2(interests):
    for user_interests in interests:
        user_id = user_interests["usuaruo"]
        for interest in user_interests["interesses"]:
            for key, score in interest.items():
                redis_conn.zadd(f"user:{user_id}:interests", {key: score})

    # Recuperando e ordenando os dados para validação
    output = []
    for user_interests in interests:
        user_id = user_interests["usuaruo"]
        interests_list = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)
        output.append(interests_list)

    return output


def test_questao_2():
    interests = [
        {"usuaruo": 1, "interesses": [{"futebol":0.855}, {"pagode":0.765}, {"engraçado":0.732}, {"cerveja":0.622}, {"estética":0.519}]},
        {"usuaruo": 2, "interesses": [{"estética":0.765}, {"jiujitsu":0.921}, {"luta":0.884}, {"academia":0.541}, {"maquiagem":0.658}]},
        {"usuaruo": 3, "interesses": [{"tecnologia":0.999}, {"hardware":0.865}, {"games":0.745}, {"culinária":0.658}, {"servers":0.54}]},
        {"usuaruo": 4, "interesses": [{"neurociências":0.865}, {"comportamento":0.844}, {"skinner":0.854}, {"laboratório":0.354}, {"pesquisa":0.428}]}
    ]

    output = [
        [('estética', 0.519), ('cerveja', 0.622), ('engraçado', 0.732), ('pagode', 0.765), ('futebol', 0.855)], 
        [('laboratório', 0.354), ('pesquisa', 0.428), ('comportamento', 0.844), ('skinner', 0.854), ('neurociências', 0.865)], 
        [('servers', 0.54), ('culinária', 0.658), ('games', 0.745), ('hardware', 0.865), ('tecnologia', 0.999)], 
        [('academia', 0.541), ('maquiagem', 0.658), ('estética', 0.765), ('luta', 0.884), ('jiujitsu', 0.921)]
    ]

    assert output == questao_2(interests)


def questao_3(posts):
    current_time = datetime.now()

    # Limpeza de posts antigos
    for key in redis_conn.keys("post:*"):
        post_time = datetime.strptime(redis_conn.hget(key, "data_hora"), "%Y-%m-%d %H:%M:%S")
        if current_time - post_time > timedelta(hours=5):
            redis_conn.delete(key)

    # Armazenamento dos novos posts
    for post in posts:
        post_key = f"post:{post['id']}"
        redis_conn.hmset(post_key, {
            "autor": post["autor"],
            "data_hora": post["data_hora"],
            "conteudo": post["conteudo"],
            "palavras_chave": post["palavras_chave"]
        })

    # Recuperação dos posts para validação
    retrieved_posts = []
    for post in posts:
        post_key = f"post:{post['id']}"
        if redis_conn.exists(post_key):
            post_data = redis_conn.hgetall(post_key)
            post_data["id"] = post["id"]
            retrieved_posts.append(post_data)

    return retrieved_posts


def test_questao_3():
    posts = [
        {"id": '345', "autor":"news_fc@g.com", "data_hora": "2024-06-10 19:51:03", "conteudo": "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!", "palavras_chave": "brasileirao, futebol, cartola, esporte" },
        {"id": '348', "autor":"gastro_pub@g.com", "data_hora": "2024-06-10 19:55:13", "conteudo": "Aprenda uma receita rápida de onion rings super crocantes.", "palavras_chave": "onion rings, receita, gastronomia, cerveja, culinária" },
        {"id": '349', "autor":"make_with_tina@g.com", "data_hora": "2024-06-10 19:56:44", "conteudo": "A dica de hoje envolve os novos delineadores da linha Rare Beauty", "palavras_chave": "maquiagem, estética, beleza, delineador" },
        {"id": '350', "autor":"samarantes@g.com", "data_hora": "2024-06-10 19:56:48", "conteudo": "Eu quando acho a chuteira que perdi na última pelada...", "palavras_chave": "pelada, futebol, cerveja, parceiros" },
        {"id": '351', "autor":"portal9@g.com", "data_hora": "2024-06-10 19:57:02", "conteudo": "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.", "palavras_chave": "neurociências, tecnologia, foco, medicamento" },
        {"id": '352', "autor":"meme_e_cia@g.com", "data_hora": "2024-06-10 19:58:33", "conteudo": "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?", "palavras_chave": "entretenimento, engraçado, viral, meme" },
        {"id": '353', "autor":"rnd_hub@g.com", "data_hora": "2024-06-10 19:59:59", "conteudo": "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada.", "palavras_chave": "comportamento, ciência, pesquisa, damasco" }
    ]

    assert posts == sorted(questao_3(posts), key=lambda d: d['id'])


def questao_4(user_id):
    current_time = datetime.now()

    # Recuperar interesses do usuário
    interests = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)
    user_interests = {interest: score for interest, score in interests}

    # Recuperar e filtrar posts recentes
    recent_posts = []
    for key in redis_conn.keys("post:*"):
        post = redis_conn.hgetall(key)
        post_time = datetime.strptime(post["data_hora"], "%Y-%m-%d %H:%M:%S")
        if current_time - post_time <= timedelta(hours=5):
            recent_posts.append(post)

    # Calcular a relevância dos posts
    posts_with_relevance = []
    for post in recent_posts:
        relevance = 0
        for keyword in post["palavras_chave"].split(", "):
            if keyword in user_interests:
                relevance += user_interests[keyword]
        posts_with_relevance.append((post["conteudo"], relevance))

    # Ordenar os posts pela relevância
    sorted_posts = sorted(posts_with_relevance, key=lambda x: x[1], reverse=True)

    # Retornar apenas os conteúdos dos posts ordenados pela relevância
    return [content for content, _ in sorted_posts]


def test_questao_4():
    user_id = 3

    output = [
        "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.",
        "Aprenda uma receita rápida de onion rings super crocantes.",
        "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada...",
        "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?",
        "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada."               
    ]

    assert output == questao_4(user_id)


def questao_5(user_views, user_id):
    current_time = datetime.now()

    # Armazenar a lista de posts vistos por cada usuário
    for view in user_views:
        usuario = view["usuario"]
        for post_id in view["visualizado"]:
            redis_conn.sadd(f"user:{usuario}:views", post_id)

    # Recuperar a lista de posts vistos pelo usuário especificado
    user_seen_posts = redis_conn.smembers(f"user:{user_id}:views")

    # Recuperar interesses do usuário
    interests = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)
    user_interests = {interest: score for interest, score in interests}

    # Recuperar e filtrar posts recentes
    recent_posts = []
    for key in redis_conn.keys("post:*"):
        post = redis_conn.hgetall(key)
        post_time = datetime.strptime(post["data_hora"], "%Y-%m-%d %H:%M:%S")
        if current_time - post_time <= timedelta(hours=5):
            if post["id"] not in user_seen_posts:
                recent_posts.append(post)

    # Calcular a relevância dos posts não vistos
    posts_with_relevance = []
    for post in recent_posts:
        relevance = 0
        for keyword in post["palavras_chave"].split(", "):
            if keyword in user_interests:
                relevance += user_interests[keyword]
        posts_with_relevance.append((post["conteudo"], relevance))

    # Ordenar os posts pela relevância
    sorted_posts = sorted(posts_with_relevance, key=lambda x: x[1], reverse=True)

    # Retornar apenas os conteúdos dos posts ordenados pela relevância
    return [content for content, _ in sorted_posts]


def test_questao_5():
    user_id = 3
    user_views = [
        {"usuario": 1, "visualizado": [345, 350, 353]},
        {"usuario": 2, "visualizado": [350, 351]},
        {"usuario": 3, "visualizado": [345, 351, 352, 353]},
        {"usuario": 4, "visualizado": []}
    ]

    output = [
        "Aprenda uma receita rápida de onion rings super crocantes.",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada..."
    ]

    assert output == questao_5(user_views, user_id)


# Executando os testes
test_questao_1()
test_questao_2()
test_questao_3()
test_questao_4()
test_questao_5()
