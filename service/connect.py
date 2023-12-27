import psycopg2


class Connect:

    def __init__(self):
        config = dict(
            dbname="livraria_bd",
            user="postgres", password="postgres",
            host="localhost", port="5432"
        )
        self._connection = psycopg2.connect(**config)

    def create_tables(self):
        from modules.cliente.dao import DAOCliente
        from modules.livro.dao import DAOLivro
        # from modules.produto.dao import DAOProduto
        cursor = self._connection.cursor()
        # cursor.execute(DAOMarca().create_table())
        cursor.execute(DAOCliente().create_table())
        cursor.execute(DAOLivro().create_table())
        self._connection.commit()
        cursor.close()

    def get_instance(self):
        return self._connection