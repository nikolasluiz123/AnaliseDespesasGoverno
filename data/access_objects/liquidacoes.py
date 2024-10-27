from pandas import DataFrame

from data.access_objects.common import DAO


class LiquidacoesDAO(DAO):

    def get_dataframe_top5_favorecidos(self,
                                       subitem: str = None,
                                       unidade_gestora: str = None) -> DataFrame:
        query_select = """
            select liquidacao.favorecido as favorecido,
                   sum(empenho.valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = """ 
            from despesas_empenho empenho
            inner join despesas_liquidacao_empenho_impactados liquidacao_empenho on empenho.codigo_empenho = liquidacao_empenho.codigo_empenho
            inner join despesas_liquidacao liquidacao on liquidacao_empenho.codigo_liquidacao = liquidacao.codigo_liquidacao 
        """

        query_where = " where 1=1 "
        where_clauses = []

        if subitem is not None:
            where_clauses.append(f" and liquidacao_empenho.subitem = '{subitem}' ")

        if unidade_gestora is not None:
            where_clauses.append(f" and liquidacao.unidade_gestora = '{unidade_gestora}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by liquidacao.favorecido "
        order_by = " order by valor desc "
        limit = " limit 5; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {order_by}
            {limit}
        """

        df = self.helper.get_dataframe(query)
        df['favorecido'] = df['favorecido'].apply(lambda x: self.insert_break_line(x, text_wrap_limit=16))

        return df

    def get_dataframe_top5_sub_itens(self, unidade_gestora: str = None) -> DataFrame:
        query_select = """
            select liquidacao_empenho.subitem as subitem,
                   sum(empenho.valor_do_empenho_convertido_pra_r) as valor
        """

        query_from = """ 
            from despesas_empenho empenho
            inner join despesas_liquidacao_empenho_impactados liquidacao_empenho on empenho.codigo_empenho = liquidacao_empenho.codigo_empenho
            inner join despesas_liquidacao liquidacao on liquidacao_empenho.codigo_liquidacao = liquidacao.codigo_liquidacao 
        """

        query_where = " where 1=1 "
        where_clauses = []

        if unidade_gestora is not None:
            where_clauses.append(f" and liquidacao.unidade_gestora = '{unidade_gestora}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by liquidacao_empenho.subitem "
        order_by = " order by valor desc "
        limit = " limit 5; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {order_by}
            {limit}
        """

        df = self.helper.get_dataframe(query)
        df['subitem'] = df['subitem'].apply(lambda x: self.insert_break_line(x, text_wrap_limit=16))

        return df

    def get_dataframe_top10_diferenca_valor_empenho_liquidado(self,
                                                              subitem: str = None,
                                                              unidade_gestora: str = None) -> DataFrame:
        query_select = """
            select liquidacao_empenho.subitem as subitem,
                   sum(empenho.valor_do_empenho_convertido_pra_r) as valor_empenho,
                   sum(liquidacao_empenho.valor_liquidado_r) as valor_liquidado
        """

        query_from = """ 
            from despesas_empenho empenho
            inner join despesas_liquidacao_empenho_impactados liquidacao_empenho on empenho.codigo_empenho = liquidacao_empenho.codigo_empenho
            inner join despesas_liquidacao liquidacao on liquidacao_empenho.codigo_liquidacao = liquidacao.codigo_liquidacao
        """

        query_where = " where 1=1 "
        where_clauses = []

        if subitem is not None:
            where_clauses.append(f" and liquidacao_empenho.subitem = '{subitem}' ")

        if unidade_gestora is not None:
            where_clauses.append(f" and liquidacao.unidade_gestora = '{unidade_gestora}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by liquidacao_empenho.subitem "
        order_by = " order by valor_liquidado desc, valor_empenho desc, subitem "
        limit = " limit 5; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {order_by}
            {limit}
        """

        df = self.helper.get_dataframe(query)

        df['subitem'] = df['subitem'].apply(self.insert_break_line)
        df.columns = ['subitem', 'Empenho', 'Liquidado']

        return df

    def get_dataframe_top5_unidades_gestoras(self, subitem: str = None) -> DataFrame:
        query_select = """
            select liquidacao.unidade_gestora as unidade, 
                   count(liquidacao.unidade_gestora) as quantidade_liquidacoes
        """

        query_from = """ 
            from despesas_liquidacao_empenho_impactados liquidacao_empenho
            inner join despesas_liquidacao liquidacao on liquidacao_empenho.codigo_liquidacao = liquidacao.codigo_liquidacao
        """

        query_where = " where 1=1 "
        where_clauses = []

        if subitem is not None:
            where_clauses.append(f" and liquidacao_empenho.subitem = '{subitem}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by liquidacao.unidade_gestora "
        order_by = " order by quantidade_liquidacoes desc, unidade "
        limit = " limit 5; "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {order_by}
            {limit}
        """

        return self.helper.get_dataframe(query)
