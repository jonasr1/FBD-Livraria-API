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

    def _process_result(self, cursor, result):
        if result is not None:
            cols = [desc[0] for desc in cursor.description]
            if isinstance(result, tuple):#Result
                result_dict = dict(zip(cols, result))
                cliente_instance = Cliente(**result_dict)
                return cliente_instance
            elif isinstance(result, list):#Results
                results = [dict(zip(cols, i)) for i in result]
                results = [Cliente(**i) for i in results]
                return results
            print("Resultado inesperado:", result)
        print("Sem resultados. Método | _process_result")
        return None

    def get_by_nome(self, nome):
        query = self._SELECT_BY_NOME
        cursor = self.connection.cursor()

        # Para buscar todas as linhas que começam com a sequência fornecida, usa-se o %
        cursor.execute(query, (f"{nome}%",))

        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def get_by_query(self, query, param):
        cursor = self.connection.cursor()
        cursor.execute(query, (param,))
        results = cursor.fetchone()
        return self._process_result(cursor, results)

    def get_by_cpf(self, cpf):
        query = self._SELECT_BY_CPF
        return self.get_by_query(query, cpf)

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        return self.get_by_query(query, id)

    def delete_by_id(self, id):
        result = self.get_by_id(id)
        if not result:
            return None, "Cliente não encontrado"
        query = self._CONSULTAR_PEDIDO
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))

        existe_pedido = cursor.fetchone()[0]

        if existe_pedido:
            return None, "O cliente possui pelo menos um pedido."

        try:
            query = self._DELETE_BY_ID
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id,))
                self.connection.commit()
                return result, "Cliente deletado com sucesso"
        except Exception as e:
            print(f"Erro ao deletar cliente: {str(e)}")
            self.connection.rollback()
            raise

    def update_cliente_by_id(self, id, data):
        try:
            query = "UPDATE cliente SET "
            set_clauses = []
            cliente_antigo = self.get_by_id(id)
            if not cliente_antigo:
                return None, "Cliente não encontrado"
            for campo in SQLCliente._CAMPOS_UPDATE:
                novo_valor = data.get(campo, '').strip()
                if campo in data.keys() and novo_valor:
                    if novo_valor == getattr(cliente_antigo, campo):
                        return None, f"Nenhum campo foi atualizado, pois campo {campo} fornecido não pode ser igual ao anterior"
                    set_clauses.append(f"{campo} = '{data.get(campo)}'")

            if not set_clauses:
                return None, "Nenhum campo fornecido para atualização"

            query += ", ".join(set_clauses)
            query += f" WHERE id = {id};"

            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()

            cliente_atualizado = self.get_by_id(id)

            return cliente_atualizado.to_dict(), "Cliente atualizado com sucesso"

        except Exception as e:
            print(f"Erro ao atualizar cliente: {str(e)}")
            self.connection.rollback()
            raise

