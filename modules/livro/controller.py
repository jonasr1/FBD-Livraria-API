import traceback
from datetime import datetime

from flask import Blueprint, request, jsonify

from modules.livro.dao import DAOLivro
from modules.livro.modelo import Livro
from modules.livro.sql import SQLivro

livro_controller = Blueprint('livro_controller', __name__)
dao_livro = DAOLivro()
module_name = 'livros'


@livro_controller.route(f'/{module_name}/preco/<int:preco>', methods=['GET'])
def get_livro_by_preco(preco: int):
    print("preco")
    livros = dao_livro.get_by_preco_aproximado(preco)
    return handle_result(livros)


@livro_controller.route(f'/{module_name}/<int:id>', methods=['PUT'])
def update_preco(id: int):
    data = request.json
    preco = data.get('preco')
    print("Preco:", preco)
    erros = []
    preco = validate_numeric_preco(preco, erros)
    if preco is None or not preco.strip(''):
        erros.append({'error': "Preco não fornecido"})
    if erros:
        return jsonify(erros), 404
    updated_preco = dao_livro.update_preco_by_id(id, preco)
    if updated_preco is not None:
        return jsonify(
            {'message': f"Preço atualizado com sucesso para {preco}", 'dados': updated_preco.__dict__}), 200
    return jsonify({'message': f"Não foi encontrado livro o id {id}.", 'dados': {}}), 404


@livro_controller.route(f'/{module_name}/<int:id>', methods=['DELETE'])
def delete_livro(id: int):
    try:
        deleted_livro = dao_livro.delete_by_id(id)
        if deleted_livro is not None:
            return jsonify({'message': "Livro deletado com sucesso", 'dados': deleted_livro.__dict__}), 200
        return jsonify({'message': f"Livro com id {id} não existe", 'dados': {}}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao deletar livro: {str(e)}"}), 500


def get_livros():
    livros = dao_livro.get_all()
    return handle_result(livros)


def create_livro():
    data = request.json
    if 'id' in data and data['id']:
        return jsonify("O ID não deve ser fornecido, pois é autoincremento."), 400
    erros = []
    for campo in SQLivro._CAMPOS_OBRIGATORIOS:
        valor_campo = data.get(campo, '')
        if campo == SQLivro._COL_PRECO:
            validate_numeric_preco(valor_campo, erros)
        if campo == SQLivro._COL_QUANTIDADE_ESTOQUE:
            validate_quantity(valor_campo, erros)
        if campo == SQLivro._COL_PRECO or campo == SQLivro._COL_QUANTIDADE_ESTOQUE:
            continue  # Não entra no validate_required quando é preço ou quantidade por causa do strip()
        validate_required(campo, data, erros)
    if erros:
        return jsonify(erros), 404
    try:
        data_publicacao = datetime.strptime(data['data_publicacao'], '%Y-%m-%d')
    except ValueError:
        return jsonify("A data de publicação deve estar no formato YYYY-MM-DD"), 400
    instance_livro = dao_livro.get_by_livro(data.get('titulo'), data.get('autor'), data_publicacao)
    if instance_livro is not None:
        return jsonify({'message': "Já existe um livro com o mesmo nome, autor e data de publicação",
                        'dados': instance_livro.to_dict()}), 404
    livro = Livro(**data)
    print(livro)
    livro = dao_livro.salvar(livro)
    return jsonify('OK'), 201


@livro_controller.route(f'/{module_name}', methods=['GET', 'POST'])
def get_or_create_livros():
    if request.method == 'GET':
        return get_livros()
    return create_livro()


def handle_result(result):
    if result:
        if isinstance(result, list):
            return jsonify([livro.to_dict() for livro in result]), 200
        return jsonify(result.to_dict()), 200
    return jsonify("Sem resultados para busca!"), 404


@livro_controller.route(f'/{module_name}/<id>', methods=['GET'])
def get_livro_by_id(id: int):
    print('id', id)
    livro = dao_livro.get_by_id(id)
    return handle_result(livro)


def get_livro(param, tipo: str):
    if tipo not in ['titulo', 'genero', 'autor']:
        return jsonify("Tipo de consulta inválido"), 401
    livros = dao_livro.get_livro_by(tipo, param)
    return handle_result(livros)


@livro_controller.route(f'/{module_name}/genero/<genero>', methods=['GET'])
def get_livro_genero(genero):
    return get_livro(genero, 'genero')


@livro_controller.route(f'/{module_name}/titulo/<titulo>', methods=['GET'])
def get_livro_titulo(titulo):
    return get_livro(titulo, 'titulo')


@livro_controller.route(f'/{module_name}/autor/<autor>', methods=['GET'])
def get_livro_autor(autor):
    return get_livro(autor, 'autor')


def convert_to_string(valor_campo):
    return str(valor_campo) if type(valor_campo) != str else valor_campo


def validate_numeric_preco(valor_campo, erros):
    valor_campo = convert_to_string(valor_campo)
    if not valor_campo.replace('.', '', 1).isdigit():
        erros.append({'preco': "35.99", 'message': f"O campo preço deve ser um valor numérico positivo fornecido como o exibido"})
    return valor_campo


def validate_quantity(valor_campo, erros):
    valor_campo = convert_to_string(valor_campo)
    if not valor_campo.isdigit() or int(valor_campo) <= 0:
        erros.append({ 'quantidade_estoque': 23, 'message': "Insira um valor inteiro positivo para a quantidade em estoque fornecido como o exibido "})


def validate_required(campo, data, erros):
    if campo not in data.keys() or not data.get(campo, '').strip():
        erros.append(f"O campo {campo} é obrigatório")

