class Pedido():
    def __init__(self, id_cliente, id=None, data_hora=None):
        self.id = id
        self.id_cliente = id_cliente
        self.data_hora = data_hora

    def __str__(self):
        return f"Pedido:{self.id_cliente}"

    def to_dict(self):
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'data_hora': self.data_hora.strftime('%Y-%m-%d %H:%M')
        }
