from modules.cliente.modelo import Cliente
from modules.cliente.sql import SQLCliente
from service.connect import Connect


class DAOCliente(SQLCliente):
    def __init__(self, ):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise Exception("Tipo inválido")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (cliente.nome, cliente.endereco, cliente.cpf,))
        self.connection.commit()
        return cliente

    def get_by_nome(self, nome):
        query = self._SELECT_BY_NOME
        cursor = self.connection.cursor()

        # Para buscar todas as linhas que começam com a sequência fornecida, usa-se o %
        cursor.execute(query, (f"{nome}%",))

        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Cliente(**i) for i in results]
        return results

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Cliente(**i) for i in results]
        return results

    def get_by_query(self, query, param):
        cursor = self.connection.cursor()
        cursor.execute(query, (param,))
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        if results:
            result_dict = results[0]
            cliente_instance = Cliente(**result_dict)
            return cliente_instance
        return None

    def get_by_cpf(self, cpf):
        query = self._SELECT_BY_CPF
        return self.get_by_query(query, cpf)

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        return self.get_by_query(query, id)

    def delete_by_id(self, id):
        result = self.get_by_id(id)
        if not result:
            return None
        try:
            query = self._DELETE_BY_ID
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id,))
                self.connection.commit()
                return result
        except Exception as e:
            print(f"Erro ao deletar cliente: {str(e)}")
            self.connection.rollback()
            raise

    def update_endereco_by_id(self, id, endereco):
        result = self.get_by_id(id)
        if not result:
            return None
        try:
            query = self._UPDATE_BY_ID
            with self.connection.cursor() as cursor:
                cursor.execute(query, (endereco, id))
                self.connection.commit()
                return result
        except Exception as e:
            print(f"Erro ao atualizar cliente por ID: {str(e)}")
            self.connection.rollback()
            raise
