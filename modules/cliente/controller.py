from flask import Blueprint, request, jsonify
from modules.cliente.dao import DAOCliente
from modules.cliente.modelo import Cliente
from modules.cliente.sql import SQLCliente

cliente_controller = Blueprint('cliente_controller', __name__)
dao_cliente = DAOCliente()
module_name = 'cliente'


def get_clientes():
    clientes = dao_cliente.get_all()
    results = [cliente.__dict__ for cliente in clientes]
    response = jsonify(results)
    response.status_code = 200
    return response


def create_cliente():
    data = request.json
    erros = []
    for campo in SQLCliente._CAMPOS_OBRIGATORIOS:
        if campo not in data.keys() or not data.get(campo, '').strip():
            erros.append(f"O campo {campo} é obrigatorio")
    if dao_cliente.get_by_cpf(**data):
        erros.append(f"Já existe um cliente com esse cpf")
    if erros:
        response = jsonify(erros)
        response.status_code = 401
        return response

    cliente = Cliente(**data)
    cliente = dao_cliente.salvar(cliente)
    print(cliente)
    response = jsonify('OK')
    response.status_code = 201
    return response


@cliente_controller.route(f'/{module_name}/', methods=['GET', 'POST'])
def get_or_create_clientes():
    if request.method == 'GET':
        return get_clientes()
    else:
        return create_cliente()


@cliente_controller.route(f'/{module_name}/<id>/', methods=['GET'])
def get_categoria_by_id(id: int):
    print('id', id)
    categoria = dao_cliente.get_id(id)
    if categoria:
        return jsonify(categoria.__dict__), 200
    return jsonify("A categoria não existe"), 404


