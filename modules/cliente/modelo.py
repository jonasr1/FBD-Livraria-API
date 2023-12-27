class Cliente():
    def __init__(self, nome, endereco, cpf, id=None):
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf

    def __str__(self):
        return f"Cliente: {self.nome}, {self.endereco}, {self.cpf}"
