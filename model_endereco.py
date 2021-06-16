class Endereco:
    def __init__(self, cidade, estado, logradouro, id_cliente, cep, id_endereco=None):
        self.id_endereco = id_endereco
        self.cidade = cidade
        self.estado = estado
        self.logradouro = logradouro
        self.id_cliente = id_cliente
        self.cep = cep