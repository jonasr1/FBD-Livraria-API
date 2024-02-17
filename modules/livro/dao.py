from modules.livro.modelo import Livro
from modules.livro.sql import SQLivro
from service.connect import Connect


class DAOLivro(SQLivro):
    def __init__(self, ):
        self.description = None
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, livro: Livro):
        if not isinstance(livro, Livro):
            raise Exception("Tipo inválido")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (livro.titulo, livro.autor, livro.genero, livro.quantidade_estoque, livro.preco, livro.data_publicacao,))
        self.connection.commit()
        return livro

    def _process_result(self, cursor, result):
        if result is not None:
            cols = [desc[0] for desc in cursor.description]
            if isinstance(result, tuple):  # Result
                result_dict = dict(zip(cols, result))
                livro_instance = Livro(**result_dict)
                return livro_instance
            elif isinstance(result, list):  # Results
                results = [dict(zip(cols, i)) for i in result]
                results = [Livro(**i) for i in results]
                return results
            else:
                print("Resultado inesperado:", result)
        return None

    def get_all(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return self._process_result(cursor, results)

    def _get_by_query(self, query, param):
        cursor = self.connection.cursor()
        cursor.execute(query, (param,))
        # Para buscar todas as linhas que começam com a sequência fornecida, usa-se o %
        cursor.execute(query, (f"{param}%",))
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

    def _execute_query(self, query, params):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return True

    def delete_by_id(self, id):
        result = self.get_by_id(id)
        if not result:
            return None
        try:
            query = self._DELETE_BY_ID
            if self._execute_query(query, (id,)):
                return result  # Para ser exibido qual o dado foi deletado
        except Exception as e:
            print(f"Erro ao deletar livro: {str(e)}")
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

    def get_by_livro(self, titulo, autor, data_publicacao):
        cursor = self.connection.cursor()
        query = self._SELECT_BY_TITULO_AUTOR_DATA
        cursor.execute(query, (titulo.lower(), autor.lower(), data_publicacao,))
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
        except Exception as e:
            print(f"Erro ao atualizar preco do livro por ID: {str(e)}")
            self.connection.rollback()
            raise
