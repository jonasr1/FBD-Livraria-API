import traceback

from flask import Blueprint, request, jsonify
from modules.cliente.dao import DAOCliente
from modules.cliente.modelo import Cliente
from modules.cliente.sql import SQLCliente

cliente_controller = Blueprint('cliente_controller', __name__)
dao_cliente = DAOCliente()
module_name = 'clientes'


@cliente_controller.route(f'/{module_name}/<int:id>', methods=['PUT'])
def update_cliente(id: int):
    try:
        dados_atualizados = request.json
        cpf = dao_cliente.validar_cpf(dados_atualizados.get('cpf'))
        if not cpf:
            return jsonify("O cpf não é valido!"), 200
        cliente_atualizado, mensagem = dao_cliente.update_cliente_by_id(id, dados_atualizados, cpf)
        if cliente_atualizado:
            return jsonify({'message': mensagem, 'dados': cliente_atualizado}), 200
        else:
            return jsonify({'message': mensagem}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao processar a solicitação de atualização: {str(e)}"}), 500


@cliente_controller.route(f'/{module_name}/<int:id>', methods=['DELETE'])
def delete_cliente(id: int):
    try:
        success, message = dao_cliente.delete_by_id(id)
        if success is not None:
            return jsonify({'message': message, 'dados': success}), 200
        return jsonify({'message': message, 'dados': {}}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao deletar cliente: {str(e)}"}), 500


def get_clientes():
    clientes = dao_cliente.get_all()
    results = [cliente.to_dict() for cliente in clientes]
    return jsonify(results), 200


'''
CPF's TESTES
44337897046
95438460060
95438460060
11740903080
53402644088
52456894057
52456894057
88936798090
70439921090
67632085025
86812008010
33358407047
'''


def create_cliente():
    data = request.json
    if 'id' in data and data['id']:
        return jsonify("O ID não deve ser fornecido, pois é autoincremento."), 400
    erros = []
    for campo in SQLCliente._CAMPOS_OBRIGATORIOS:
        if campo == 'cpf':
            valor = str(data.get(campo, ''))
            if isinstance(valor, str) and not valor.strip():
                erros.append(f"O campo {campo} é obrigatório")
            elif not isinstance(valor, str) and not valor:
                erros.append(f"O campo {campo} é obrigatório")
            continue
        if campo not in data.keys() or not data.get(campo, '').strip():
            erros.append(f"O campo {campo} é obrigatorio")
    cpf = dao_cliente.validar_cpf(data.get('cpf'))
    if not cpf:
        return jsonify("O cpf não é valido!"), 200
    if dao_cliente.get_by_cpf(cpf):
        erros.append("Já existe um cliente com esse cpf")
    if erros:
        return jsonify(erros), 200
    try:
        cliente = Cliente(**data)
        cliente = dao_cliente.salvar(cliente, cpf)
        return jsonify('OK'), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao processar a solicitação de atualização: {str(e)}"}), 500


@cliente_controller.route(f'/{module_name}', methods=['GET', 'POST'])
def get_or_create_clientes():
    if request.method == 'GET':
        return get_clientes()
    return create_cliente()


def get_cliente_by_id(id: int):
    cliente = dao_cliente.get_by_id(id)
    return handle_result(cliente)


@cliente_controller.route(f'/{module_name}/cpf/<cpf>', methods=['GET'])
def get_cliente_by_cpf(cpf):
    cliente = dao_cliente.get_by_cpf(cpf)
    return handle_result(cliente)


def get_clientes_by_nome(identificador):
    clientes = dao_cliente.get_by_nome(identificador)
    return handle_result(clientes)


@cliente_controller.route(f'/{module_name}/<path:identificador>', methods=['GET'])
def get_cliente_by_nome_or_id(identificador):
    if identificador.isdigit():  # Se o identificador for um número, assume que é um id
        return get_cliente_by_id(identificador)
    return get_clientes_by_nome(identificador)


def handle_result(result):
    if result:
        if isinstance(result, list):
            return jsonify([cliente.to_dict() for cliente in result]), 200
        return jsonify(result), 200
    return jsonify("O cliente não existe"), 200
