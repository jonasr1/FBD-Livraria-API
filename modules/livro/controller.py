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
    livros = dao_livro.get_by_preco_aproximado(preco)
    return handle_result(livros)


@livro_controller.route(f'/{module_name}/<int:id>', methods=['PUT'])
def update_livro(id: int):
    global data_publicacao
    livro_antigo = dao_livro.get_by_id(id)
    if not livro_antigo:
        return jsonify("Livro não encontrado"), 200
    data = request.json
    if 'id' in data and data['id']:
        return jsonify("O ID não deve ser fornecido, pois é autoincremento."), 400
    erros = []
    for campo in SQLivro._CAMPOS_VERIFICAR_PUT:
        valor_campo = data.get(campo, '')
        if campo == SQLivro._COL_PRECO and campo in data:
            validate_numeric_preco(valor_campo, erros)
        if campo == SQLivro._COL_QUANTIDADE_ESTOQUE and campo in data:
            validate_quantity(valor_campo, erros)
        if campo == SQLivro._COL_PRECO or campo == SQLivro._COL_QUANTIDADE_ESTOQUE:
            continue  # Não entra no validate_required quando é preço ou quantidade por causa do strip()
        validate_required(campo, data, erros)
    if erros:
        return jsonify(erros), 404
    try:
        if 'data_publicacao' in data:
            data_publicacao = datetime.strptime(data['data_publicacao'], '%Y-%m-%d')
    except ValueError:
        return jsonify("A data de publicação deve estar no formato YYYY-MM-DD"), 400
    if 'titulo' in data and 'genero' in data and 'autor' in data and 'data_publicacao' in data:
        instance_livro = dao_livro.get_by_livro(data.get('titulo'), data.get('genero'), data.get('autor'),
                                                data_publicacao)
        if instance_livro is not None:
            return jsonify({'message': "Já existe um livro com o mesmo título, gênero, autor e data de publicação",
                            'dados': instance_livro}), 404
    livro_atualizar, mensagem = dao_livro.update_livro(id, data, livro_antigo)
    try:
        if livro_atualizar:
            return jsonify({'message': mensagem, 'dados': livro_atualizar}), 200
        else:
            return jsonify({'message': mensagem}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Erro ao processar a solicitação de atualização: {str(e)}"}), 500


@livro_controller.route(f'/{module_name}/<int:id>', methods=['DELETE'])
def delete_livro(id: int):
    try:
        deleted_livro = dao_livro.delete_by_id(id)
        if deleted_livro is not None:
            return jsonify({'message': "Livro deletado com sucesso", 'dados': deleted_livro.to_dict()}), 200
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
    quantidade = None
    for campo in SQLivro._CAMPOS_OBRIGATORIOS:
        valor_campo = data.get(campo, '')
        if campo == SQLivro._COL_PRECO:
            validate_numeric_preco(valor_campo, erros)
        if campo == SQLivro._COL_QUANTIDADE_ESTOQUE:
            quantidade, validate_quantity(valor_campo, erros)
        if campo == SQLivro._COL_PRECO or campo == SQLivro._COL_QUANTIDADE_ESTOQUE:
            continue  # Não entra no validate_required quando é preço ou quantidade por causa do strip()
        validate_required(campo, data, erros)
    if erros:
        return jsonify(erros), 404
    try:
        data_publicacao = datetime.strptime(data['data_publicacao'], '%Y-%m-%d')
    except ValueError:
        return jsonify("A data de publicação deve estar no formato YYYY-MM-DD"), 400
    instance_livro = dao_livro.get_by_livro(data.get('titulo'), data.get('genero'), data.get('autor'), data_publicacao)
    if instance_livro is not None:
        return jsonify({'message': "Já existe um livro com o mesmo título, gênero, autor e data de publicação",
                        'dados': instance_livro.to_dict()}), 404
    livro = Livro(**data)
    livro = dao_livro.salvar(livro, quantidade)
    return jsonify('OK'), 201


@livro_controller.route(f'/{module_name}', methods=['GET', 'POST'])
def get_or_create_livros():
    if request.method == 'GET':
        return get_livros()
    return create_livro()


@livro_controller.route(f'/{module_name}/<id>', methods=['GET'])
def get_livro_by_id(id: int):
    livro = dao_livro.get_by_id(id)
    return handle_result(livro)


@livro_controller.route(f'/{module_name}/genero/<genero>', methods=['GET'])
def get_livro_genero(genero):
    return get_livro(genero, 'genero')


@livro_controller.route(f'/{module_name}/titulo/<titulo>', methods=['GET'])
def get_livro_titulo(titulo):
    return get_livro(titulo, 'titulo')


@livro_controller.route(f'/{module_name}/autor/<autor>', methods=['GET'])
def get_livro_autor(autor):
    return get_livro(autor, 'autor')


def get_livro(param, tipo: str):
    if tipo not in ['titulo', 'genero', 'autor']:
        return jsonify("Tipo de consulta inválido"), 401
    livros = dao_livro.get_livro_by(tipo, param)
    return handle_result(livros)


def remover_adicionar_estoque_livro(id: int, operacao: str):
    try:
        quantidade = request.json.get('quantidade_estoque')
        erros = []
        quantidade = validate_quantity(quantidade, erros)
        if erros:
            return jsonify(erros), 412
        livro = dao_livro.get_by_id(id)
        if livro is None:
            return jsonify({'message': f'O livro de ID {id} não foi encontrado'}), 404
        livro_update = dao_livro.remover_adicionar_estoque(operacao, quantidade, id)
        return jsonify({'message': f'A quantidade do livro foi atualizada de {livro.get("quantidade_estoque")} para {livro_update.get("quantidade_estoque")}.','livro': livro_update}), 200
    except Exception:
        traceback.print_exc()
        return jsonify({'error': 'Ocorreu um erro ao manipular o estoque do livro'}), 500


@livro_controller.route(f'/{module_name}/<int:id>/adicionar-estoque', methods=['POST'])
def adicionar_estoque_livro(id: int):
    return remover_adicionar_estoque_livro(id, "adicionar")


@livro_controller.route(f'/{module_name}/<int:id>/remover-estoque', methods=['POST'])
def remover_estoque_livro(id: int):
    return remover_adicionar_estoque_livro(id, "remover")


def handle_result(result):
    if result:
        if isinstance(result, list):
            return jsonify([livro.to_dict() for livro in result]), 200
        return jsonify(result.to_dict()), 200
    return jsonify("Sem resultados para busca!"), 404


def convert_to_string(valor_campo):
    return str(valor_campo) if type(valor_campo) != str else valor_campo


def validate_numeric_preco(valor_campo, erros):
    valor_campo = convert_to_string(valor_campo)
    if not valor_campo.replace('.', '', 1).isdigit():
        erros.append({'preco': "35.99",
                      'message': f"O campo preço deve ser um valor numérico positivo fornecido como o exibido"})
    return valor_campo


def validate_quantity(valor_campo, erros):
    valor_campo = convert_to_string(valor_campo)
    if not valor_campo.isdigit() or int(valor_campo) <= 0:
        erros.append({'message': "Insira um valor inteiro positivo para a quantidade em estoque"})
    return valor_campo


def validate_required(campo, data, erros):
    if campo not in data.keys() or not data.get(campo, '').strip():
        erros.append(f"O campo {campo} é obrigatório")
