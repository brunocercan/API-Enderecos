class EnderecoDAO:
    def __init__(self, db):
        self.__db = db
        
    def salvar(self, endereco):
        cursor = self.__db.connection.cursor()
        cursor.execute('INSERT INTO endereco (cidade, estado, logradouro, id_cliente, cep) values (%s, %s, %s, %s, %s)', (endereco.cidade, endereco.estado, endereco.logradouro, endereco.id_cliente, endereco.cep))
        endereco.id_endereco = cursor.lastrowid
        self.__db.connection.commit()
        return endereco

    def deletar(self, id):
        self.__db.connection.cursor().execute('delete from endereco where id_endereco = %s', (id, ))

    def alterar(self, endereco, id):
        cursor = self.__db.connection.cursor()
        cursor.execute('UPDATE endereco SET cidade=%s, estado=%s, logradouro=%s, id_cliente=%s, cep=%s where id_endereco=%s', (endereco.cidade, endereco.estado, endereco.logradouro, endereco.id_cliente, endereco.cep, id))
        return endereco