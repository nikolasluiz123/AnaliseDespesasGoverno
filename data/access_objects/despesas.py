import pandas as pd
from pandas import DataFrame

from data.access_objects.common import DAO


class DespesaEmpenhoDAO(DAO):

    def get_dataframe_quantidade_categorias(self,
                                            tipo_credito: str=None,
                                            tipo_operacao: str=None,
                                            funcao: str=None) -> DataFrame:
        query_select = """
            select empenho.categoria_de_despesa as categoria,
                   count(*) as quantidade
        """

        query_from = """ 
            from despesas_empenho empenho 
        """

        query_where = " where 1=1 "
        where_clauses = []

        if tipo_credito is not None:
            where_clauses.append(f" and empenho.tipo_credito = '{tipo_credito}' ")

        if tipo_operacao is not None:
            query_from += " inner join despesas_item_empenho_historico historico on empenho.id_empenho = historico.id_empenho "
            where_clauses.append(f" and historico.tipo_operacao = '{tipo_operacao}' ")

        if funcao is not None:
            where_clauses.append(f" and empenho.funcao = '{funcao}' ")

        if  len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by empenho.categoria_de_despesa; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
        """

        return self.helper.get_dataframe(query)

    def get_dataframe_valor_categoria_tempo(self,
                                            tipo_credito: str=None,
                                            categoria_despesa: str=None,
                                            funcao: str = None,
                                            tipo_operacao: str = None) -> DataFrame:
        query_select = """
           select empenho.data as data,
                  empenho.categoria_de_despesa as categoria,
                  avg(empenho.valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = """
            from despesas_empenho empenho
        """

        query_where = " where 1=1 "
        where_clauses = []

        if tipo_credito is not None:
            where_clauses.append(f" and empenho.tipo_credito = '{tipo_credito}' ")

        if categoria_despesa is not None:
            where_clauses.append(f" and empenho.categoria_de_despesa = '{categoria_despesa}' ")

        if funcao is not None:
            where_clauses.append(f" and empenho.funcao = '{funcao}' ")

        if tipo_operacao is not None:
            query_from += " inner join despesas_item_empenho_historico historico on empenho.id_empenho = historico.id_empenho "
            where_clauses.append(f" and historico.tipo_operacao = '{tipo_operacao}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by empenho.data, empenho.categoria_de_despesa "
        query_order_by = " order by empenho.data desc; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {query_order_by}
        """

        df = self.helper.get_dataframe(query)
        df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')

        return df

    def get_dataframe_valores_tipo_credito(self,
                                           categoria_despesa: str = None,
                                           funcao: str = None,
                                           tipo_operacao: str = None) -> DataFrame:
        query_select = """
            select empenho.tipo_credito as tipo,
            avg(empenho.valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = """ 
            from despesas_empenho empenho 
        """

        query_where = " where 1=1 "
        where_clauses = []

        if categoria_despesa is not None:
            where_clauses.append(f" and empenho.categoria_de_despesa = '{categoria_despesa}' ")

        if funcao is not None:
            where_clauses.append(f" and empenho.funcao = '{funcao}' ")

        if tipo_operacao is not None:
            query_from += " inner join despesas_item_empenho_historico historico on empenho.id_empenho = historico.id_empenho "
            where_clauses.append(f" and historico.tipo_operacao = '{tipo_operacao}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by empenho.tipo_credito "
        order_by = " order by empenho.valor_do_empenho_convertido_pra_r desc; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {order_by}
        """

        return self.helper.get_dataframe(query)

    def get_dataframe_top5_funcoes_maior_investimento(self,
                                                      categoria_despesa: str = None,
                                                      tipo_credito: str = None,
                                                      tipo_operacao: str = None) -> DataFrame:
        query_select = """
            select empenho.funcao as funcao,
                   sum(empenho.valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = """ 
            from despesas_empenho empenho 
        """

        query_where = " where 1=1 "
        where_clauses = []

        if categoria_despesa is not None:
            where_clauses.append(f" and empenho.categoria_de_despesa = '{categoria_despesa}' ")

        if tipo_credito is not None:
            where_clauses.append(f" and empenho.tipo_credito = '{tipo_credito}' ")

        if tipo_operacao is not None:
            query_from += " inner join despesas_item_empenho_historico historico on empenho.id_empenho = historico.id_empenho "
            where_clauses.append(f" and historico.tipo_operacao = '{tipo_operacao}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by funcao "
        query_order_by = " order by valor desc "
        query_limit = " limit 5; "

        query = f"""
                    {query_select}
                    {query_from}
                    {query_where}
                    {query_group_by}
                    {query_order_by}
                    {query_limit}
                """

        return self.helper.get_dataframe(query)

    def get_dataframe_quantidade_tipo_operacao(self,
                                               categoria_despesa: str = None,
                                               tipo_credito: str = None,
                                               funcao: str = None) -> DataFrame:
        query_select = """
            select historico.tipo_operacao as tipo, 
                   count(*) as quantidade
        """

        query_from = """ 
            from despesas_item_empenho_historico historico 
        """

        if categoria_despesa is not None or tipo_credito is not None or funcao is not None:
            query_from += " inner join despesas_empenho empenho on empenho.id_empenho = historico.id_empenho "

        query_where = " where 1=1 "
        where_clauses = []

        if categoria_despesa is not None:
            where_clauses.append(f" and empenho.categoria_de_despesa = '{categoria_despesa}' ")

        if tipo_credito is not None:
            where_clauses.append(f" and empenho.tipo_credito = '{tipo_credito}' ")

        if funcao is not None:
            where_clauses.append(f" and empenho.funcao = '{funcao}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by historico.tipo_operacao "
        query_order_by = " order by quantidade desc "

        query = f"""
                    {query_select}
                    {query_from}
                    {query_where}
                    {query_group_by}
                    {query_order_by}
                """

        return self.helper.get_dataframe(query)