from modules.item_pedido.modelo import ItemPedido
from modules.item_pedido.sql import SQLItemPedido
from modules.livro.dao import DAOLivro
from modules.livro.modelo import Livro
from service.connect import Connect


class DAOItemPedido(SQLItemPedido):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def salvar(self, item_pedido:ItemPedido):
        global novo_estoque
        if not isinstance(item_pedido, ItemPedido):
            raise Exception("Tipo inválido")
        for campo in SQLItemPedido._CAMPOS_VERIFICAR:
            id = item_pedido.__getattribute__(campo)
            result = self.get_by_id_pedido(id) if campo == 'id_pedido' else self.get_by_id_livro(id)
            if not result:
                raise Exception(f"O {campo} = {id} não existe")
        livro = self.get_by_id_livro(item_pedido.id_livro)
        if livro is None:
            raise ValueError("Livro não encontrado")
        if livro:
            novo_estoque = livro[4] - item_pedido.quantidade
            if novo_estoque < 0:
                raise Exception("Quantidade em estoque insuficiente")
        try:
            self.atualizar_quantidade_estoque(item_pedido.id_livro, novo_estoque)
            query = self._INSERT_INTO
            cursor = self.connection.cursor()
            cursor.execute(query, (item_pedido.id_pedido, item_pedido.id_livro, item_pedido.quantidade,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        return item_pedido

    def atualizar_quantidade_estoque(self, livro_id, novo_estoque):
        query = self._ATUALIZAR_ESTOQUE_LIVRO
        cursor = self.connection.cursor()
        cursor.execute(query, (novo_estoque, livro_id))
        self.connection.commit()

    def delete_by_id(self, id):
        item_pedido, cursor_i_p = self.get_by_id_objeto(id)
        if not item_pedido:
            return None
        try:
            livro = self.get_by_id_livro(item_pedido[2])
            query = self._DELETE_BY_ID
            novo_estoque = livro[4] + item_pedido[3]
            self.atualizar_quantidade_estoque(item_pedido[2], novo_estoque)
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id,))
                self.connection.commit()
                return self._process_result(cursor_i_p, item_pedido)
        except Exception:
            self.connection.rollback()
            raise

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return self._process_result(cursor, result)

    def get_by_id_objeto(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result, cursor

    def get_by_id_pedido(self, id_pedido):
        query = self._SELECT_BY_ID_PEDIDO
        return self.get_by_query_no_process(query, id_pedido)

    def get_by_id_livro(self, id_livro):
        query = self._SELECT_BY_ID_LIVRO
        return self.get_by_query_no_process(query, id_livro)

    def get_by_query_no_process(self, query, param):
        cursor = self.connection.cursor()
        cursor.execute(query, (param,))
        result = cursor.fetchone()
        return result

    @staticmethod
    def _process_result(cursor, result):
        if result is not None:
            cols = [desc[0] for desc in cursor.description]
            if isinstance(result, tuple):  # Result
                result_dict = dict(zip(cols, result))
                pedido_instance = ItemPedido(**result_dict)
                return pedido_instance.to_dict()
            elif isinstance(result, list):  # Results
                results = [dict(zip(cols, i)) for i in result]
                results = [ItemPedido(**i) for i in results]
                return results
            raise Exception("Resultado inesperado:", result)
        return None

    def get_item_pedidos_pedido(self, id_pedido):
        query = self._ITENS_PEDIDOS_PEDIDO
        cursor = self.connection.cursor()
        cursor.execute(query, (id_pedido,))
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def update_item_by_id(self, id, data):
        try:
            for campo in SQLItemPedido._CAMPOS_VERIFICAR:
                id_campos_verificar = data.get(campo)
                result = self.get_by_id_pedido(id_campos_verificar) if campo == 'id_pedido' else self.get_by_id_livro(id_campos_verificar)
                if not result:
                    raise Exception(f"O {campo} = {id_campos_verificar} não existe")
            query = "UPDATE item_pedido SET "
            set_clauses = []
            item_antigo = self.get_by_id(id)
            if not item_antigo:
                return None, "Item pedido não encontrado"
            for campo in SQLItemPedido._CAMPOS_UPDATE:
                novo_valor = data.get(campo)
                if campo in data.keys() and novo_valor:
                    if novo_valor == getattr(item_antigo, campo):
                        return None, f"Nenhum campo foi atualizado, pois campo {campo} fornecido não pode ser igual ao anterior"
                    set_clauses.append(f"{campo} = '{data.get(campo)}'")
            if not set_clauses:
                return None, "Nenhum campo fornecido para atualização"
            query += ", ".join(set_clauses)
            query += f" WHERE id = {id};"
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
            item_atualizado = self.get_by_id(id)
            return item_atualizado.__dict__, "Item pedido atualizado com sucesso"
        except Exception:
            self.connection.rollback()
            raise

