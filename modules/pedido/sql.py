class SQLPedido:
    _TABLE_NAME = "Pedido"
    _COL_ID = "id"
    _COL_ID_CLIENTE = "id_cliente"
    _COL_DATA_HORA = "data_hora"

    _CREATE_TABLE = f'create table IF NOT EXISTS {_TABLE_NAME} (id serial primary key,'\
                    f'{_COL_ID_CLIENTE} INT not null,'\
                    f'{_COL_DATA_HORA} timestamp(0) DEFAULT CURRENT_TIMESTAMP,'\
                    f'FOREIGN key (id_cliente) REFERENCES cliente(id));'

    #timestamp(0) DEFAULT CURRENT_TIMESTAMP, -- Ajuste para incluir apenas data, hora e segundo

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}({_COL_ID_CLIENTE}) values(%s)'

    _SELECT_ALL = f"SELECT * from {_TABLE_NAME}"
    _SELECT_BY_ID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"
    _SELECT_BY_ID_CLIENTE = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID_CLIENTE} = %s"

    _DELETE_BY_ID = f"DELETE FROM {_TABLE_NAME} WHERE {_COL_ID} = %s"
    _DELETE_BY_ID_CLIENTE = f"DELETE FROM {_TABLE_NAME} WHERE {_COL_ID_CLIENTE} = %s"

    _PEDIDOS_CLIENTE = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID_CLIENTE} = %s;"
    _CONSULTAR_PEDIDO = f"SELECT EXISTS (SELECT 1 FROM item_pedido WHERE id_pedido = %s);"
    _EXIST_CLIENTE =  f"SELECT * FROM cliente WHERE {_COL_ID} = %s"
    _UPDATE_PEDIDO = f"UPDATE {_TABLE_NAME} SET {_COL_ID_CLIENTE} = %s, {_COL_DATA_HORA} = CURRENT_TIMESTAMP WHERE {_COL_ID} = %s"

