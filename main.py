from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from model_endereco import Endereco
from dao_endereco import EnderecoDAO
from functools import wraps
import jsons

app = Flask(__name__)
db = MySQL(app)
app.config.from_pyfile('db_config.py')
endereco_dao = EnderecoDAO(db)

#================================================== AUTENTICAÇÃO ================================================#

def login(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      login = request.authorization
      if login and login.username == 'login' and login.password == 'senha':
         return f(*args, *kwargs)
      else:
         return make_response('Login ou senha incorreto!', 401, {'WWW-Authenticate' : 'Basic realm="Necessario Login"'})
   return decorated

# ================================================  ROTAS =======================================================#


@app.route('/')
@login
def index():
    return jsonify({'API': 'ENDEREÇOS'})

@app.route('/enderecos/listar')
def get():
   lista = listar(db)
   return jsonify(jsons.dump(lista))

@app.route('/enderecos/buscar/<int:id>')
def buscar(id):
    try:
        endereco = filtrar_por_id(db,id)
    except:
        pass
        return jsonify('id: cliente invalido')
    else:
        return jsonify(jsons.dump(endereco))
        
@app.route('/enderecos/cadastrar', methods=['POST', ])
def post():
    cidade = request.json['cidade']
    estado = request.json['estado']
    logradouro = request.json['logradouro']
    id_cliente = request.json['id_cliente']
    cep = request.json['cep']

    id_cliente = verifica_id_cliente(db, id_cliente)

    if id_cliente == None:
        return jsonify('id cliente invalido')
    else:
        endereco = Endereco(cidade, estado, logradouro, id_cliente, cep)
        endereco_dao.salvar(endereco)
        return jsonify('ENDERECO CADASTRADO COM SUCESSO!', jsons.dump(endereco))

@app.route('/enderecos/alterar/<int:id>', methods=['PUT', ])
def put(id):
    if verifica_id_endereco(db, id) == None:
        return jsonify('id_endereco: {} invalido'.format(id))
    else:
        cidade = request.json['cidade']
        estado = request.json['estado']
        logradouro = request.json['logradouro']
        cep = request.json['cep']
        id_cliente = request.json['id_cliente']

        if verifica_id_cliente(db, id_cliente) == None:
            return jsonify('id_cliente: {} invalido'.format(id_cliente))
        else:
            endereco = Endereco(cidade, estado, logradouro, id_cliente, cep, id)
            endereco_dao.alterar(endereco, id)
            return jsonify('ENDERECO ALTERADO COM SUCESSO!', jsons.dump(endereco))

@app.route('/enderecos/deletar/<int:id>', methods = ['DELETE', ])
def delete(id):
    if verifica_id_endereco(db, id) == None:
        return jsonify('id_endereco: {} invalido'.format(id))
    else:
        endereco_dao.deletar(id)
        return jsonify('endereço id: {} deletado com sucesso!'.format(id))
    

#=====================================================   MÉTODOS    ====================================#


def filtrar_por_id(db, id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_endereco, cidade, estado, logradouro, id_cliente, cep from endereco where id_cliente = %s', (id, ))
    endereco = converte_endereco(cursor.fetchall())
    return endereco

def verifica_id_cliente(db, id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id from clientes where id=%s', (id, ))
    id_cliente = cursor.fetchone()
    return id_cliente

def verifica_id_endereco(db, id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id_endereco from endereco where id_endereco=%s', (id, ))
    id_endereco = cursor.fetchone()
    return id_endereco

def converte_endereco(enderecos):
    def cria_endereco_com_tupla(tupla):
        return jsons.dump(Endereco(id_endereco=tupla[0], cidade=tupla[1], estado=tupla[2], logradouro=tupla[3], id_cliente=tupla[4], cep=tupla[5]))
    return list(map(cria_endereco_com_tupla, enderecos))

def listar(db):
        cursor = db.connection.cursor()
        cursor.execute('SELECT id_endereco, cidade, estado, logradouro, id_cliente, cep from endereco')
        enderecos = converte_endereco(cursor.fetchall())
        return enderecos

app.run()