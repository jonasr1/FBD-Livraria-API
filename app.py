# Connect to your postgres DB

from flask import Flask

from modules.cliente.controller import cliente_controller
from modules.item_pedido.controller import item_pedido_controller
from modules.livro.controller import livro_controller
from modules.pedido.controller import pedido_controller
from service.connect import Connect

app = Flask(__name__)
app.register_blueprint(cliente_controller)
app.register_blueprint(livro_controller)
app.register_blueprint(pedido_controller)
app.register_blueprint(item_pedido_controller)
Connect().create_tables()
print("Pedido: OK\nLivro:VER\nItem_pedido:OK\nCliente:VER")
app.run(debug=True)
