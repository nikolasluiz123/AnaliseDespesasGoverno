import re
import sqlite3

import pandas as pd
import unicodedata
from pandas import DataFrame
from tabulate import tabulate


class SQLite3Helper:
    """
    Classe helper para execução de comandos SQL e controle de conexão.
    """

    def __init__(self, db_name):
        """
        :param db_name: Nome do arquivo de banco
        """

        self.conn = sqlite3.connect(f'data/{db_name}.db', check_same_thread=False)

    def has_table(self, table_name) -> bool:
        """
        Função que retorna se a tabela passada como parâmetro existe.

        :param table_name: Nome da tabela
        """

        query = f"select name from sqlite_master where type='table' and name='{table_name}';"
        name = self.conn.execute(query).fetchone()

        return name is not None

    def create_database(self, urls: dict[str, str]):
        """
        Função que realiza a criação do db. Essa operação é executada apenas quando não existir a tabela com o nome
        definido na chave do dicionário de urls.

        :param urls: Dicionário com as chaves que vão ser o nome das tabelas e as urls que apontam para o arquivo csv.
        """

        print('Iniciando criação do DB...')

        for file_name, local_file_path in urls.items():
            if not self.has_table(file_name):
                df = pd.read_csv(local_file_path, encoding='ISO-8859-1', on_bad_lines='skip', sep=';', low_memory=False)
                df = self.__normalize_columns(df)
                df.to_sql(file_name, self.conn, index=False, if_exists='replace')
                print(f'Tabela {file_name} criada com sucesso!')

        self.__create_tables_index()

        print()
        print('DB criado com sucesso!')

    def __create_tables_index(self):
        """
        Função para criar os índices necessários para que os filtros realizados nos dashboards sejam performáticos.
        """
        self.execute_sql('create index if not exists idx_id_empenho on despesas_empenho (id_empenho);')
        self.execute_sql('create index if not exists idx_tipo_credito on despesas_empenho (tipo_credito);')
        self.execute_sql('create index if not exists idx_categoria_de_despesa on despesas_empenho (categoria_de_despesa);')
        self.execute_sql('create index if not exists idx_funcao on despesas_empenho (funcao);')
        self.execute_sql('create index if not exists idx_codigo_empenho on despesas_empenho (codigo_empenho);')

        self.execute_sql('create index if not exists idx_id_empenho_item on despesas_item_empenho (id_empenho);')
        self.execute_sql('create index if not exists idx_id_empenho_historico on despesas_item_empenho_historico (id_empenho);')
        self.execute_sql('create index if not exists idx_tipo_operacao on despesas_item_empenho_historico (tipo_operacao);')

        self.execute_sql('create index if not exists idx_codigo_empenho_impactados on despesas_liquidacao_empenho_impactados (codigo_empenho);')
        self.execute_sql('create index if not exists idx_codigo_liquidacao_empenho_impactados on despesas_liquidacao_empenho_impactados (codigo_liquidacao);')

        self.execute_sql('create index if not exists idx_codigo_liquidacao on despesas_liquidacao (codigo_liquidacao);')

    def __normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Percorre as colunas do dataframe e normaliza o nome das colunas para um padrão mais comum em banco de dados.

        :param df: DataFrame com os dados
        """

        df.columns = [self.__normalize_column_name(col) for col in df.columns]

        return df

    def __normalize_column_name(self, name: str) -> str:
        """
        Realiza a normalização do nome da coluna utilizando unicodedata e regex.

        :param name: Nome da coluna
        """

        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
        name = re.sub(r'\W+', '_', name)

        return name.strip('_').lower()

    def close_connection(self):
        """
        Função que deve ser utilizada ao fim das execuções para fechar a conexão com o banco.
        """

        self.conn.close()

    def get_first(self, sql: str):
        """
        Função que pode ser utilizada para obter o primeiro registro de alguma query.

        :param sql: Consulta que deseja obter o primeiro resultado.
        """
        return self.conn.execute(sql).fetchone()

    def execute_sql(self, sql: str):
        """
        Função que pode ser utilizada para executar um comando sql qualquer.

        :param sql: Comando sql
        """

        return self.conn.execute(sql)

    def get_dataframe(self, sql: str) -> DataFrame:
        """
        Função que pode ser utilizada para obter um DataFrame de um select

        :param sql: Sql com o select desejado
        """

        return pd.read_sql(sql, self.conn)

    @staticmethod
    def show_dataframe(df: DataFrame):
        """
        Função utilizada para exibição do DataFrame no console.

        :param df: DataFrame que deseja exibir
        """
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))