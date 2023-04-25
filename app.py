from flask import Flask, jsonify, request
import mysql.connector
banco = mysql.connector.connect( #conecção com o banco de dados
    host='localhost',
    user='root',
    password='',
    database='api',
    port='3306'
)

app = Flask(__name__) #cria uma aplicação flask e atribui a variavel app

@app.route('/usuario', methods=['GET'])
def get_usuario():
    cursor = banco.cursor()
    sql = f'SELECT * FROM usuarios'
    cursor.execute(sql)
    usuarios_bruto = cursor.fetchall()
    cursor.close()
    usuarios_lapdado = list()
    for x in usuarios_bruto:
        usuarios_lapdado.append(
            {
            'id': x[0],
             'nome': x[1], 
             'login': x[2], 
             'senha': x[3]
             }
        )

    return jsonify(mensagem='Lista dos usuarios', dados=usuarios_lapdado)


@app.route('/usuario', methods=['POST'])
def get_usuarioid():
    novo_usuario = request.json
    cursor = banco.cursor()
    sql = f"insert into usuarios(id, nome, login, senha) values('{novo_usuario['id']}','{novo_usuario['nome']}','{novo_usuario['login']}','{novo_usuario['senha']}')"
    cursor.execute(sql)
    cursor.close()
    banco.commit()#registrar a transação
    return jsonify(mensagem='usuario cadastrado com sucesso')


@app.route('/usuario/<int:id>', methods=['GET'])
def get_usuario_id(id):
    cursor = banco.cursor()
    sql = f"select id, nome, login, senha from usuarios where id={id}"
    cursor.execute(sql)
    resposta = cursor.fetchall()
    if(resposta != []): #manutenção preventiva por que pode retornar mais de um mesmo dado;?
        usuario = list()
        usuario.append(
                        {
                        'id': resposta[0][0],
                        'nome': resposta[0][1],
                        'login': resposta[0][2],
                        'senha': resposta[0][3]
                        }
                        )
        return jsonify(dados = usuario, mensagem='listando o usuario requisitado')
    else:
        return {'erro':'Pessoa não encontrada'}, 404
    
@app.route('/usuario/login/<string:login>', methods=['GET'])
def get_usuario_login(login):
    cursor = banco.cursor()
    sql = f"select id, nome, login, senha from usuarios where login='{login}'"
    cursor.execute(sql)
    retorno = cursor.fetchall()
    if retorno != []:
        usuario = list()
        usuario.append(
                        {
                        'id': retorno[0][0],
                        'nome': retorno[0][1],
                        'login': retorno[0][2],
                        'senha': retorno[0][3]
                        }
                        )
        return jsonify(dados = usuario, mensagem='listando o usuario requisitado')
    else:
        return {'erro':'Pessoa não encontrada'}, 404
    
@app.route('/usuario/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    cursor = banco.cursor()
    sql_pesquisar = f'select id from usuarios where id={id}'
    sql_delete = f"delete from usuarios where id={id}"
    cursor.execute(sql_pesquisar)
    pesquisa = cursor.fetchall()
    if pesquisa != []:
        cursor.execute(sql_delete)
        banco.commit()
        return jsonify(mensagem='usuario deletado')
    else:
        return jsonify(mensagem='Usuario não encontrado para deletar')
    

@app.route('/usuario/<int:id>', methods=['PUT']) #arumar para não quebra quando foi inserido um unico lugar para atualiar ou doi 
def atualizar_usuario(id):
    atualizacao = request.json
    cursor = banco.cursor()
    sql_pesquisa = f"select id from usuarios where id={id}"
    cursor.execute(sql_pesquisa)
    resposta = cursor.fetchall()
    if resposta != []:
        sql_update = f"update usuarios set id='{atualizacao['id']}', nome='{atualizacao['nome']}', login='{atualizacao['login']}', senha='{atualizacao['senha']}' where id='{id}'"
        cursor.execute(sql_update)
        banco.commit()
        return jsonify(mensagem='usuario atualizado com sucesso')
    else:
        return jsonify(mensagem='não foi possivel achar usuario para atualizar')
app.run(port=5000, host='localhost', debug=False)
banco.close()
