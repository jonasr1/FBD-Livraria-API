from modules.cliente.modelo import Cliente
from modules.cliente.sql import SQLCliente
from service.connect import Connect


class DAOCliente(SQLCliente):
    def __init__(self, ):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, cliente: Cliente, cpf):
        if not isinstance(cliente, Cliente):
            raise Exception("Tipo inválido")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (cliente.nome, cliente.endereco, cpf,))
        self.connection.commit()
        return cliente

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
            return None, "O cliente possui pelo menos um pedido associado a ele."
        try:
            query = self._DELETE_BY_ID
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id,))
                self.connection.commit()
                return result, "Cliente deletado com sucesso"
        except Exception:
            self.connection.rollback()
            raise

    def update_cliente_by_id(self, id, data, cpf):
        try:
            exist_cpf = self.get_by_cpf(cpf)
            if exist_cpf:
                return None, f"O CPF já registrado"
            set_clauses = []
            cliente_antigo = self.get_by_id(id)
            if not cliente_antigo:
                return None, "Cliente não encontrado"
            quant_campos = 0  # N° de campos para atualizar
            n_reptidos = 0
            for campo in SQLCliente._CAMPOS_UPDATE:
                if campo == 'cpf':
                    continue
                novo_valor = data.get(campo, '').strip()
                if campo in data.keys() and novo_valor:
                    quant_campos += 1
                    if novo_valor == cliente_antigo[campo]:
                        n_reptidos += 1
                        continue
                    set_clauses.append(f"{campo} = '{data.get(campo)}'")
            if quant_campos == n_reptidos:
                return None, "Cliente não atualizado, pois os dados são iguais aos registrados"
            if not set_clauses:
                return None, "Nenhum campo fornecido para atualização"
            set_clause_str = ", ".join(set_clauses)
            query = f"UPDATE cliente SET {set_clause_str} WHERE id = {id};"
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
            cliente_atualizado = self.get_by_id(id)
            return cliente_atualizado, "Cliente atualizado com sucesso"
        except Exception:
            self.connection.rollback()
            raise

    def validar_cpf(self, cpf: str):
        """
        Efetua a validação do CPF, tanto formatação quanto dígitos verificadores.

        Parâmetros:
        cpf (str): CPF a ser validado

        Retorno:
        bool:
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.
        """
        cpf = cpf if isinstance(cpf, str) else str(cpf)
        # Obtém apenas os números do CPF, ignorando pontuações
        numeros = [int(digito) for digito in cpf if digito.isdigit()]
        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numeros) != 11 or len(set(numeros)) == 1:
            return False
        # Validação do primeiro dígito verificador:
        soma_produtos = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
        digito_esperado = (soma_produtos * 10 % 11) % 10
        if numeros[9] != digito_esperado:
            return False
        # Validação do segundo dígito verificador:
        soma_produtos = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
        digito_esperado = (soma_produtos * 10 % 11) % 10
        if numeros[10] != digito_esperado:
            return False
        return ''.join(map(str, numeros))

    @staticmethod
    def _process_result(cursor, result):
        if result is not None:
            cols = [desc[0] for desc in cursor.description]
            if isinstance(result, tuple):  # Result
                result_dict = dict(zip(cols, result))
                cliente_instance = Cliente(**result_dict)
                return cliente_instance.to_dict()
            elif isinstance(result, list):  # Results
                results = [dict(zip(cols, i)) for i in result]
                results = [Cliente(**i) for i in results]
                return results
            raise Exception("Resultado inesperado:", result)
        return None
