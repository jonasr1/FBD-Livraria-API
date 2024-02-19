from modules.livro.sql import SQLivro


class SQLItemPedido:
    _TABLE_NAME = "item_pedido"
    _COL_ID = "id"
    _COL_ID_PEDIDO = "id_pedido"
    _COL_ID_LIVRO = "id_livro"
    _COL_QUANTIDADE = "quantidade"
    _COL_PRECO_UNITARIO = "preco_unitario"
    _CAMPOS_OBRIGATORIOS = [_COL_ID_PEDIDO, _COL_ID_LIVRO, _COL_QUANTIDADE]
    _CAMPOS_PROIBIDOS = [_COL_ID, _COL_PRECO_UNITARIO]
    _CAMPOS_UPDATE = _CAMPOS_OBRIGATORIOS
    _CAMPOS_VERIFICAR = [_COL_ID_PEDIDO, _COL_ID_LIVRO]

    _CREATE_TABLE = f'create table IF NOT EXISTS {_TABLE_NAME} ({_COL_ID} serial primary key,' \
                    f' {_COL_ID_PEDIDO} int not null,' \
                    f'{_COL_ID_LIVRO} int not null,' \
                    f'{_COL_QUANTIDADE} int not null,' \
                    f'{_COL_PRECO_UNITARIO} decimal,' \
                    f'FOREIGN key ({_COL_ID_PEDIDO}) references pedido({_COL_ID}),' \
                    f'FOREIGN key ({_COL_ID_LIVRO}) references livro({_COL_ID}));'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}({_COL_ID_PEDIDO}, {_COL_ID_LIVRO}, {_COL_QUANTIDADE}) values(%s, %s, %s)'
    _SELECT_ALL = f"SELECT * from {_TABLE_NAME}"
    _SELECT_BY_ID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"
    _DELETE_BY_ID = f"DELETE FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"
    _ITENS_PEDIDOS_PEDIDO = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID_PEDIDO} = %s;"

    _SELECT_BY_ID_PEDIDO = f"SELECT * FROM pedido WHERE {_COL_ID} = %s"
    _SELECT_BY_ID_LIVRO = f"SELECT * FROM livro WHERE {_COL_ID} = %s"

    _CONSULTAR_PEDIDO = f"SELECT EXISTS (SELECT 1 FROM item_pedido WHERE id_pedido = %s);"
    _ATUALIZAR_ESTOQUE_LIVRO = f"UPDATE {SQLivro._TABLE_NAME} SET {SQLivro._COL_QUANTIDADE_ESTOQUE} = %s WHERE {SQLivro._COL_ID} = %s"
