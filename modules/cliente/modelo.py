class Cliente():
    def __init__(self, nome, endereco, cpf, id=None):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf

    def __str__(self):
        return 'Cliente: {}, {}, {}'.format(self.nome, self.endereco, self.cpf)

    # def __str__(self):
    #     return f"Cliente: {self.nome}, {self.endereco}, {self.cpf}"

