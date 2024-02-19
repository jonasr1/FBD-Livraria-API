class Livro():
    def __init__(self, titulo, autor, genero, quantidade_estoque, preco, data_publicacao, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.quantidade_estoque = quantidade_estoque
        self.preco = preco
        self.data_publicacao = data_publicacao

    def __str__(self):
        return f"Livro: {self.titulo}, {self.autor}, {self.genero}, {self.quantidade_estoque}, {self.preco}, {self.data_publicacao}"

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'genero': self.genero,
            'quantidade_estoque': self.quantidade_estoque,
            'preco': self.preco,
            'data_publicacao': self.data_publicacao.strftime('%Y-%m-%d') if self.data_publicacao else None
        }
