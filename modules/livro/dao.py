from modules.livro.modelo import Livro
from modules.livro.sql import SQLivro
from service.connect import Connect


class DAOLivro(SQLivro):
    def __init__(self, ):
        self.description = None
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, livro: Livro, quantidade_estoque):
        if not isinstance(livro, Livro):
            raise Exception("Tipo inválido")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (
            livro.titulo, livro.autor, livro.genero, quantidade_estoque, livro.preco, livro.data_publicacao,))
        self.connection.commit()
        return livro

    def update_livro(self, id, data, livro_antigo):
        try:
            set_clauses = []
            quant_campos = 0  # N° de campos para atualizar
            n_reptidos = 0
            for campo in SQLivro._CAMPOS_UPDATE:
                if campo == "quantidade_estoque":
                    set_clauses.append(f"{campo} = '{str(data.get(campo))}'")
                    quant_campos += 1
                    continue
                novo_valor = data.get(campo, '').strip()
                if campo in data.keys() and novo_valor:
                    quant_campos += 1
                    if novo_valor == livro_antigo[campo]:
                        n_reptidos += 1
                        continue
                    set_clauses.append(f"{campo} = '{data.get(campo)}'")
            if quant_campos == n_reptidos:
                return None, "Livro não atualizado, pois os dados são iguais aos registrados"
            if not set_clauses:
                return None, "Nenhum campo fornecido para atualização"
            set_clause_str = ", ".join(set_clauses)
            query = f"UPDATE livro SET {set_clause_str} WHERE id = {id};"
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
            livro_atualizado = self.get_by_id(id)
            return livro_atualizado, "Livro atualizado com sucesso"
        except Exception:
            self.connection.rollback()
            raise

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def get_livro_by(self, tipo, parametro):
        queries = {
            'titulo': self._SELECT_BY_TITULO,
            'autor': self._SELECT_BY_AUTOR,
            'genero': self._SELECT_BY_GENERO
        }
        query = queries.get(tipo)
        return self._get_by_query(query, parametro)

    def get_by_id(self, id):
        cursor = self.connection.cursor()
        query = self._SELECT_BY_ID
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return self._process_result(cursor, result)

    def delete_by_id(self, id):
        result = self.get_by_id(id)
        if not result:
            return None
        try:
            query = self._DELETE_BY_ID
            if self._execute_query(query, (id,)):
                return result  # Para ser exibido qual o dado foi deletado
        except Exception:
            self.connection.rollback()
            raise

    def get_by_preco_aproximado(self, preco: int):
        cursor = self.connection.cursor()
        margem_tolerancia = 5
        query = self._SELECT_BY_PRECO_APROXIMADO
        preco_minimo = preco - margem_tolerancia
        preco_maximo = preco + margem_tolerancia
        cursor.execute(query, (preco_minimo, preco_maximo), )
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def get_by_livro(self, titulo, genero, autor, data_publicacao):
        cursor = self.connection.cursor()
        query = self._SELECT_BY_TITULO_GENERO_AUTOR_DATA
        cursor.execute(query, (titulo.lower(), genero.lower(), autor.lower(), data_publicacao,))
        result = cursor.fetchone()
        return self._process_result(cursor, result)

    def update_preco_by_id(self, id, preco):
        result = self.get_by_id(id)
        if not result:
            return None
        try:
            query = self._UPDATE_PRECO_BY_ID
            if self._execute_query(query, (preco, id)):
                return result  # Para ser exibido qual o dado foi atualizado
        except Exception:
            self.connection.rollback()
            raise

    def remover_adicionar_estoque(self, operacao, quantidade, id):
        if operacao == "adicionar":
            query = self._ADICONAR_ESTOQUE
        elif operacao == "remover":
            query = self._REMOVER_ESTOQUE
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (quantidade, id,))
            self.connection.commit()
            return self.get_by_id(id)
        except Exception:
            self.connection.rollback()
            raise

    def _process_result(self, cursor, result):
        if result is not None:
            cols = [desc[0] for desc in cursor.description]
            if isinstance(result, tuple):  # Result
                result_dict = dict(zip(cols, result))
                livro_instance = Livro(**result_dict)
                return livro_instance.to_dict()
            elif isinstance(result, list):  # Results
                results = [dict(zip(cols, i)) for i in result]
                results = [Livro(**i) for i in results]
                return results
            raise Exception("Resultado inesperado:", result)
        return None

    def _get_by_query(self, query, param):
        cursor = self.connection.cursor()
        cursor.execute(query, (param,))
        # Para buscar todas as linhas que começam com a sequência fornecida, usa-se o %
        cursor.execute(query, (f"{param}%",))
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def _execute_query(self, query, params):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return True

