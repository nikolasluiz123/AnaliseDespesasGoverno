from abc import ABC

from numpy.matlib import empty
from pandas import DataFrame

from data.sqlite_db_helper import SQLite3Helper


class DAO(ABC):

    def __init__(self, helper: SQLite3Helper):
        self.helper = helper


class CategoriaDespesaDAO(DAO):

    def get_dataframe_quantidade_categorias(self, tipo_credito: str=None) -> DataFrame:
        query_select = """
            select categoria_de_despesa as categoria,
                   count(*) as quantidade
        """

        query_from = " from despesas_empenho "

        query_where = " where 1=1 "
        where_clauses = []

        if tipo_credito is not None:
            where_clauses.append(f" and tipo_credito = '{tipo_credito}' ")

        if where_clauses is not empty:
            query_where.join(where_clauses)

        query_group_by = " group by categoria_de_despesa; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
        """

        return self.helper.get_dataframe(query)

    def get_dataframe_valor_categoria_tempo(self, tipo_credito: str=None, categoria_despesa: str=None) -> DataFrame:
        query_select = """
           select data as data,
                  categoria_de_despesa as categoria,
                  avg(valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = " from despesas_empenho "

        query_where = " where 1=1 "
        where_clauses = []

        if tipo_credito is not None:
            where_clauses.append(f" and tipo_credito = '{tipo_credito}' ")

        if categoria_despesa is not None:
            where_clauses.append(f" and categoria_de_despesa = '{categoria_despesa}' ")

        if where_clauses is not empty:
            query_where += " ".join(where_clauses)

        query_group_by = " group by data, categoria_de_despesa "
        query_order_by = " order by data desc; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {query_order_by}
        """

        return self.helper.get_dataframe(query)


class TipoCreditoDAO(DAO):

    def get_dataframe_valores_tipo_credito(self, categoria_despesa: str = None) -> DataFrame:
        query_select = """
            select tipo_credito as tipo,
            avg(valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = " from despesas_empenho "

        query_where = " where 1=1 "
        where_clauses = []

        if categoria_despesa is not None:
            where_clauses.append(f" and categoria_de_despesa = '{categoria_despesa}' ")

        if where_clauses is not empty:
            query_where.join(where_clauses)

        query_group_by = " group by tipo_credito; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
        """

        return self.helper.get_dataframe(query)
