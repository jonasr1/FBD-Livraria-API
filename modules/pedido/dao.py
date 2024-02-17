from modules.pedido.modelo import Pedido
from modules.pedido.sql import SQLPedido
from service.connect import Connect


class DAOPedido(SQLPedido):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, pedido: Pedido):
        if not isinstance(pedido, Pedido):
            raise Exception("Tipo inválido")
        id_cliente = pedido.id_cliente
        result = self.exist_cliente(id_cliente)
        if not result:
            raise Exception(f"O cliente de id {id_cliente} não existe")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (id_cliente,))
        self.connection.commit()
        return pedido

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def get_by_id_cliente(self, id_cliente):
        query = self._SELECT_BY_ID_CLIENTE
        return self.get_by_query(query, id_cliente)

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        return self.get_by_query(query, id)

    def delete_by_id(self, id):
        result = self.get_by_id(id)
        if not result:
            return None, "Pedido não encontrado"
        query = self._CONSULTAR_PEDIDO
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        existe_pedido = cursor.fetchone()[0]
        if existe_pedido:
            return None, "O pedido possui pelo menos um item pedido associado."
        query = self._DELETE_BY_ID
        return self.delete_by_query(query, id, result)

    def delete_by_id_cliente(self, id_cliente):
        result = self.get_by_id_cliente(id_cliente)
        if not result:
            return None
        query = self._DELETE_BY_ID
        return self.delete_by_query(query, id_cliente, result)

    def delete_by_query(self, query, id_or_id_cliente, result):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id_or_id_cliente,))
                self.connection.commit()
                return result, "Pedido deletado com sucesso"  # Para ser exibido qual o dado foi deletado
        except Exception as e:
            print(f"Erro ao deletar pedido: {str(e)}")
            self.connection.rollback()
            raise

    def get_pedidos_clientes(self, id_cliente):
        query = self._PEDIDOS_CLIENTE
        cursor = self.connection.cursor()
        cursor.execute(query, (id_cliente,))
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def update_pedido_by_id(self, id, id_cliente):
        result = self.get_by_id(id)
        if not result:
            return None, f"O pediddo de id = {id} não existe"
        cliente = self.exist_cliente(id_cliente)
        if cliente is None:
            return None, f"O cliente de id = {id_cliente} não existe"
        try:
            query = self._UPDATE_PEDIDO
            cursor = self.connection.cursor()
            cursor.execute(query, (id_cliente, id,))
            self.connection.commit()
            return result, "Pedido atualizado com sucesso!"  # result, para ser exibido qual o dado foi atualizado
        except Exception as e:
            print(f"Erro ao atualizar id_cliente por ID: {str(e)}")
            self.connection.rollback()
            raise

    def get_by_query(self, query, param):
        cursor = self.connection.cursor()
        cursor.execute(query, (param,))
        result = cursor.fetchone()
        return self._process_result(cursor, result)

    def exist_cliente(self, id_cliente):
        query = self._EXIST_CLIENTE
        cursor = self.connection.cursor()
        cursor.execute(query, (id_cliente,))
        cliente = cursor.fetchone()
        return cliente

    @staticmethod
    def _process_result(cursor, result):
        if result is not None:
            cols = [desc[0] for desc in cursor.description]
            if isinstance(result, tuple):  # Result
                result_dict = dict(zip(cols, result))
                pedido_instance = Pedido(**result_dict)
                return pedido_instance.to_dict()
            elif isinstance(result, list):  # Results
                results = [dict(zip(cols, i)) for i in result]
                results = [Pedido(**i) for i in results]
                return results
            raise Exception("Resultado inesperado:", result)
        return None

