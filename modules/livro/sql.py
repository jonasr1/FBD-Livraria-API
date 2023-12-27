class SQLivro:
    _TABLE_NAME = "livro"
    _COL_ID = "id"
    _COL_TITULO = "titulo"
    _COL_AUTOR = "autor"
    _COL_GENERO = "genero"
    _COL_QUANTIDADE_ESTOQUE = "quantidade_estoque"
    _COL_PRECO = "preco"
    _COL_DATA_PUBLICACAO = "data_publicacao"
    _CAMPOS_OBRIGATORIOS =[_COL_TITULO, _COL_GENERO, _COL_QUANTIDADE_ESTOQUE, _COL_PRECO]

    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME}' \
                    f'(id serial primary key,' \
                    f'{_COL_TITULO} varchar(255) not null,' \
                    f'{_COL_AUTOR} varchar(255),' \
                    f'{_COL_GENERO} varchar(255),' \
                    f'{_COL_QUANTIDADE_ESTOQUE} int, ' \
                    f'{_COL_PRECO} decimal,' \
                    f'{_COL_DATA_PUBLICACAO} date);'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}({_COL_TITULO}, {_COL_AUTOR}, {_COL_GENERO}, {_COL_QUANTIDADE_ESTOQUE}, {_COL_PRECO}, {_COL_DATA_PUBLICACAO}) values(%s, %s, %s, %s, %s, %s)'
    _SELECT_BY_TITULO = f"SELECT * from {_TABLE_NAME} where {_COL_TITULO} ilike %s"
    _SELECT_BY_AUTOR = f"SELECT * from {_TABLE_NAME} where {_COL_AUTOR} ilike %s"
    _SELECT_BY_GENERO = f"SELECT * from {_TABLE_NAME} where {_COL_GENERO} ilike %s"

    _SELECT_BY_TITULO_AUTOR_DATA = f"SELECT * FROM {_TABLE_NAME} WHERE LOWER({_COL_TITULO}) ILIKE LOWER(%s) AND LOWER({_COL_AUTOR}) ILIKE LOWER(%s) AND {_COL_DATA_PUBLICACAO} = %s"

    # _SELECT_BY_TITULO_AUTOR_DATA = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_TITULO} = %s AND {_COL_AUTOR} = %s AND {_COL_DATA_PUBLICACAO} = %s"

    #tem que ver
    _SELECT_BY_PRECO_APROXIMADO = f"SELECT * from {_TABLE_NAME} WHERE {_COL_PRECO} >= %s AND {_COL_PRECO} <= %s"
    _SELECT_BY_PRECO = f"SELECT * from {_TABLE_NAME} where {_COL_PRECO} ilike %s"

    _SELECT_ALL = f"SELECT * from {_TABLE_NAME}"
    _SELECT_BY_ID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"
    _DELETE_BY_ID = f"DELETE FROM {_TABLE_NAME} WHERE id = %s"

    _UPDATE_PRECO_BY_ID = f"UPDATE {_TABLE_NAME} SET {_COL_PRECO} = %s WHERE id = %s;"

