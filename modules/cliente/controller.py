import traceback

from flask import Blueprint, request, jsonify
from modules.cliente.dao import DAOCliente
from modules.cliente.modelo import Cliente
from modules.cliente.sql import SQLCliente

cliente_controller = Blueprint('cliente_controller', __name__)
dao_cliente = DAOCliente()
module_name = 'cliente'

@cliente_controller.route(f'/{module_name}/<int:id>', methods=['PUT'])
def update_cliente(id: int):
    pass

@cliente_controller.route(f'/{module_name}/<int:id>/', methods=['DELETE'])
def delete_cliente(id: int):
    try:
        success = dao_cliente.delete_by_id(id)
        if success is not None:
            return jsonify({'message': "Cliente deletado com sucesso", 'dados': success.__dict__}), 200
        return jsonify({'message': "Cliente não existe", 'dados': {}}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao deletar cliente: {str(e)}"}), 500


def get_clientes():
    clientes = dao_cliente.get_all()
    results = [cliente.__dict__ for cliente in clientes]
    response = jsonify(results)
    response.status_code = 200
    return response


def create_cliente():
    data = request.json

    if 'id' in data and data['id']:
        return jsonify("O ID não deve ser fornecido, pois é autoincremento."), 400

    erros = []
    for campo in SQLCliente._CAMPOS_OBRIGATORIOS:
        if campo not in data.keys() or not data.get(campo, '').strip():
            erros.append(f"O campo {campo} é obrigatorio")
    if dao_cliente.get_by_cpf(data.get('cpf')):
        erros.append("Já existe um cliente com esse cpf")
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


def handle_result(result):
    if result:
        if isinstance(result, list):
            return jsonify([cliente.__dict__ for cliente in result]), 200
        else:
            return jsonify(result.__dict__), 200
    return jsonify("O cliente não existe"), 404


@cliente_controller.route(f'/{module_name}/id/<id>/', methods=['GET'])
def get_cliente_by_id(id: int):
    print('id', id)
    cliente = dao_cliente.get_by_id(id)
    return handle_result(cliente)


def get_cliente_by_cpf(identificador):
    cliente = dao_cliente.get_by_cpf(identificador)
    return handle_result(cliente)


def get_clientes_by_nome(identificador):
    clientes = dao_cliente.get_by_nome(identificador)
    return handle_result(clientes)


@cliente_controller.route(f'/{module_name}/<path:identificador>/', methods=['GET'])
def get_cliente_by_nome_or_cpf(identificador):
    """
       Retorna informações de um cliente com base no NOME ou CPF.

       Parâmetros:
       - identificador (str or int): O CPF (se for um número) ou Nome (se for uma string).

       """
    print(identificador)
    if identificador.isdigit():  # Se o identificador for um número, assume que é um CPF
        print("CPF")
        return get_cliente_by_cpf(identificador)
    else:
        print("Nome")
        return get_clientes_by_nome(identificador)
