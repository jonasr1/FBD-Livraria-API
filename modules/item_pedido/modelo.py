from modules.livro.dao import DAOLivro
from modules.pedido.dao import DAOPedido


class ItemPedido():
    def __init__(self, id_pedido, id_livro, quantidade, preco_unitario=None, id=None):
        self.id = id
        self.id_pedido = id_pedido
        self.id_livro = id_livro
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.pedido = DAOPedido().get_by_id(self.id_pedido)
        self.livro = DAOLivro().get_by_id(self.id_livro)

    def __str__(self):
        return f"Item_pedido: {self.id_pedido}, {self.id_livro}, {self.quantidade}, {self.preco_unitario}"

    def to_dict(self):
        return {
            'pedido': self.pedido,
            'livro': self.livro,
            'quantidade': self.quantidade,
            'preco_unitário': self.preco_unitario

        }

