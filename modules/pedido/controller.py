import traceback

from flask import Blueprint, request, jsonify

from modules.pedido.dao import DAOPedido
from modules.pedido.modelo import Pedido
from modules.pedido.sql import SQLPedido

pedido_controller = Blueprint('pedido_controlller', __name__)
dao_pedido = DAOPedido()
module_name = 'pedidos'


@pedido_controller.route(f'/id_cliente/<int:id_cliente>/{module_name}', methods=['GET'])
def get_pedidos_cliente_by_id(id_cliente: int):
    pedidos = dao_pedido.get_pedidos_clientes(id_cliente)
    return handle_result(pedidos)


@pedido_controller.route(f'/{module_name}/<id>', methods=['GET'])
def get_pedido_by_id(id: int):
    result = dao_pedido.get_by_id(id)
    return handle_result(result)


def get_pedidos():
    livros = dao_pedido.get_all()
    return handle_result(livros)


def create_pedido():
    data = request.json
    if ('id' in data and data['id']) or ('data_hora' in data and data['data_hora']):
        return jsonify("O ID e data não devem ser fornecidos, pois são atribuidos automaticamente"), 400
    campo = SQLPedido._COL_ID_CLIENTE
    if not data.get('id_cliente'):
        return jsonify(f"O campo {campo} é obrigatório")
    if not validate_id_cliente(data.get(campo, '')):
        return jsonify(f"O {campo} deve ser um número inteiro válido"), 401
    try:
        pedido = Pedido(**data)
        pedido = dao_pedido.salvar(pedido)
        return jsonify('OK'), 201
    except Exception as e:
        return jsonify(str(e)), 400


@pedido_controller.route(f'/{module_name}', methods=['GET', 'POST'])
def get_or_create_pedidos():
    if request.method == 'GET':
        return get_pedidos()
    return create_pedido()


@pedido_controller.route(f'/{module_name}/<int:id>', methods=['PUT'])
def update_pedido(id: int):
    try:
        data = request.json
        if ('id' in data and data['id']) or ('data_hora' in data and data['data_hora']):
            return jsonify("O ID e data não devem ser fornecidos, pois são atribuidos automaticamente"), 400
        is_id, id_cliente = validate_id_cliente(data.get('id_cliente'))
        if not id_cliente:
            return jsonify("O id_cliente deve ser um valor inteiro positivo")
        pedido, mensagem = dao_pedido.update_pedido_by_id(id, id_cliente)
        if pedido:
            return jsonify({'message': mensagem, 'dados': pedido}), 200
        return jsonify({'message': mensagem}), 404

    except Exception as e:
        print(f"Erro ao processar a solicitação de atualização: {str(e)}")
        return jsonify({"error": f"Erro ao processar a solicitação de atualização: {str(e)}"}), 500


@pedido_controller.route(f'/{module_name}/<int:id>', methods=['DELETE'])
def delete_pedido(id: int):
    try:
        success, message = dao_pedido.delete_by_id(id)
        if success is not None:
            return jsonify({'message': message, 'dados': success}), 200
        return jsonify({'message': message, 'dados': {}}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao deletar cliente: {str(e)}"}), 500


def handle_result(result):
    if result:
        if isinstance(result, list):
            return jsonify([pedido.to_dict() for pedido in result]), 200
        return jsonify(result), 200
    return jsonify("Sem resultados para busca!"), 404


def convert_to_string(valor_campo):
    return str(valor_campo) if type(valor_campo) != str else valor_campo


def validate_id_cliente(valor_campo):
    valor_campo = convert_to_string(valor_campo)
    return False if (not valor_campo.isdigit() or int(valor_campo) <= 0) else True, int(valor_campo)
