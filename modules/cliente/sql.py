class SQLCliente:
    _TABLE_NAME = "cliente"
    _COL_ID = "id"
    _COL_NOME = "nome"
    _COL_ENDERECO = "endereco"
    _COL_CPF = "cpf"
    _CAMPOS_OBRIGATORIOS = [_COL_NOME,_COL_CPF,_COL_ENDERECO]
    _CAMPOS_UPDATE = [_COL_NOME, _COL_ENDERECO, _COL_CPF]

    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME}' \
                    f'(id serial primary key,' \
                    f'{_COL_NOME} varchar(255) not null,' \
                    f'{_COL_ENDERECO} varchar(255) not null,' \
                    f'{_COL_CPF} varchar(11) not null UNIQUE);'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}({_COL_NOME}, {_COL_ENDERECO}, {_COL_CPF}) values(%s, %s, %s)'
    _SELECT_BY_NOME = f"SELECT * from {_TABLE_NAME} where {_COL_NOME} ilike %s"
    _SELECT_BY_CPF = f"SELECT * from {_TABLE_NAME} where {_COL_CPF} = %s"
    _SELECT_ALL = f"SELECT * from {_TABLE_NAME}"
    _SELECT_BY_ID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"
    _DELETE_BY_ID = f"DELETE FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"

    '''Verifica se o cliente tem algum pedido associado a ele.
    '''
    _CONSULTAR_PEDIDO = f"SELECT EXISTS (SELECT 1 FROM pedido WHERE id_cliente = %s);"
