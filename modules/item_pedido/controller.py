import traceback

from flask import Blueprint, jsonify, request

from modules.item_pedido.dao import DAOItemPedido
from modules.item_pedido.modelo import ItemPedido
from modules.item_pedido.sql import SQLItemPedido

item_pedido_controller = Blueprint('item_pedido_controlller', __name__)
dao_item_pedido = DAOItemPedido()
module_name = 'item_pedidos'


def get_itens_pedidos():
    result = dao_item_pedido.get_all()
    return handle_result(result)


@item_pedido_controller.route(f'/{module_name}/<int:id>', methods=['DELETE'])
def delete_item_pedido(id:int):
    try:
        deleted_item_pedido = dao_item_pedido.delete_by_id(id)
        if deleted_item_pedido is not None:
            return jsonify({'message': "Item pedido deletado com sucesso", 'dados': deleted_item_pedido.__dict__}), 200
        return jsonify({'message': f"O item pedido com id {id} não existe", 'dados': {}}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao deletar livro: {str(e)}"}), 500


def create_item_pedido():
    data = request.json
    if ('id' in data and data['id']) or ('preco_unitario' in data and data['preco_unitario']):
        return jsonify("O id e o preco_unitario não deve ser fornecido, pois são atribuidos automaticamente."), 400

    for campo in SQLItemPedido._CAMPOS_OBRIGATORIOS:
        valor_campo = data.get(campo)
        if valor_campo is None:
            return jsonify(f"O campo {campo} é obrigatório!")
        valor_campo = convert_to_string(valor_campo)
        if not valor_campo.isdigit() or int(valor_campo) <= 0:
            return jsonify({"error": f"O campo {campo} deve ser um valor inteiro é positivo"}), 401
    try:
        item_pedido = ItemPedido(**data)
        item_pedido = dao_item_pedido.salvar(item_pedido)
        return jsonify('OK'), 201
    except Exception as e:
        return jsonify(str(e)), 400


@item_pedido_controller.route(f'/{module_name}/<int:id>', methods=['PUT'])
def update_item_pedido(id: int):
    try:
        data = request.json
        for campo in SQLItemPedido._CAMPOS_UPDATE:
            valor_campo = convert_to_string(data.get(campo))
            if not valor_campo.isdigit() or int(valor_campo) <= 0:
                return jsonify({"error": f"O campo {campo} deve ser um valor inteiro é positivo"}), 401

        item_atualizado = ItemPedido(**data)
        item_atualizado, mensagem = dao_item_pedido.update_item_by_id(id, data)

        if item_atualizado:
            return jsonify({'message': mensagem, 'dados': item_atualizado}), 200
        else:
            return jsonify({'message': mensagem}), 404

    except Exception as e:
        print(f"Erro ao processar a solicitação de atualização: {str(e)}")
        return jsonify({"error": f"Erro ao processar a solicitação de atualização: {str(e)}"}), 500


@item_pedido_controller.route(f'/{module_name}/<int:id_pedido>/itens', methods=['GET'])
def get_pedidos_cliente_by_id(id_pedido: int):
    itens_pedidos = dao_item_pedido.get_item_pedidos_pedido(id_pedido)
    return handle_result(itens_pedidos)


@item_pedido_controller.route(f'/{module_name}/<id>', methods=['GET'])
def get_pedido_by_id(id: int):
    result = dao_item_pedido.get_by_id(id)
    return handle_result(result)


@item_pedido_controller.route(f'/{module_name}', methods=['GET', 'POST'])
def get_or_create_item_pedidos():
    if request.method == 'GET':
        return get_itens_pedidos()
    return create_item_pedido()


def handle_result(result):
    if result:
        if isinstance(result, list):
            return jsonify([item_pedido.__dict__ for item_pedido in result]), 200
        return jsonify(result.__dict__), 200
    return jsonify("Sem resultados para busca!"), 404


def convert_to_string(valor_campo):
    return str(valor_campo) if type(valor_campo) != str else valor_campo
