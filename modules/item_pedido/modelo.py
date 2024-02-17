class ItemPedido():
    def __init__(self, id_pedido, id_livro, quantidade, preco_unitario=None, id=None):
        self.id = id
        self.id_pedido = id_pedido
        self.id_livro = id_livro
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def __str__(self):
        return f"Item_pedido: {self.id_pedido}, {self.id_livro}, {self.quantidade}, {self.preco_unitario}"

