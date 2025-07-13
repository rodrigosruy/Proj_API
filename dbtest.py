import sqlite3

pt = sqlite3.connect("post.db")
cursor = pt.cursor()
# cursor.execute(f"CREATE TABLE IF NOT EXISTS posta(user TEXT, user TEXT, conteudo TEXT)")
# cursor.execute(f"SELECT seguido FROM segue WHERE seguidor='{msg.conteudoRecv}'")
# test = cursor.fetchall()

# print(test[0][0])
# candidatos = ast.literal_eval(test)
# print(candidatos)
# cursor.execute(f""" SELECT seguido FROM segue WHERE seguidor='usr1'  """)
# seguidos = cursor.fetchall()
# print(f'seguidos: {seguidos}')
# cursor.execute(f"""SELECT * FROM posta WHERE user='{msg.usuario}' """)
# cursor.execute(f"""SELECT * FROM posta""")
# test = cursor.fetchall()
# print(f'select * test: {test}')
# cursor.execute(f"SELECT conteudo FROM posta")
# posts = cursor.fetchall()


# cursor.execute("""INSERT INTO segue VALUES ('usr1', 'Julia'), ('usr1', 'Rodrigo'), ('usr1', 'Murilo'), ('Murilo', 'Rodrigo'), ('Rodrigo', 'Murilo')""")
# cursor.execute("""INSERT INTO posta VALUES ('usr1', '1', 'usr1: postei 1o'), ('Rodrigo', '2', 'Rodrigo: Teste teste'), ('Murilo', '3', 'Murilo: Odeio o elixir cara'), ('Murilo', '7', 'Murilo: Vou fazer em pithon msm')""")
# pt.commit()

# cursor.execute(f"""SELECT * FROM segue""")
# test = cursor.fetchall()
# print(f'segue table:\n{test}')

# cursor.execute(f"""SELECT * FROM posta""")
# test = cursor.fetchall()
# print(f'posta table:\n{test}')

# cursor.execute("""SELECT p.user, p.timestamp, p.conteudo FROM segue s JOIN posta p ON s.seguido = p.user WHERE s.seguidor = 'user1' ORDER BY p.timestamp DESC;""")
# test = cursor.fetchall()
# print(f'query ver post por user table:\n{test}')


usuario = 'user1'

# Query para buscar os posts e informações dos usuários seguidos
query = """
SELECT posta.user, posta.timestamp, posta.conteudo
FROM 
    posta
LEFT JOIN 
    segue ON posta.user = segue.seguido
WHERE 
    segue.seguidor = 'usr1'
ORDER BY 
    posta.timestamp ASC;
"""

# Executa a query com o parâmetro do usuário
cursor.execute(query)

# Obtém os resultados
posts = cursor.fetchall()
print(posts)
# Verifica e exibe os resultados
if posts:
    for user, conteudo in posts:
        print(f"Usuário: {user}, Post: {conteudo}")
else:
    print("Nenhum post encontrado para os usuários seguidos.")

pt.close()