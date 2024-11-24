from pandas import DataFrame

from data.access_objects.common import DAO


class PagamentosDAO(DAO):
    """
    Implementação de acesso aos dados dos Pagamentos.
    """

    def get_dataframe_top5_bancos_mais_utilizados(self, extraorcamentario: str = None) -> DataFrame:
        query_select = """
            select bancos.nome_banco as nome,
            count(bancos.nome_banco) as quantidade_pagamentos
        """

        query_from = """ 
            from despesas_pagamento_lista_bancos bancos
        """

        query_where = " where bancos.nome_banco is not null and bancos.nome_banco != '' "
        where_clauses = []

        if extraorcamentario is not None:
            query_from += " inner join despesas_pagamento pagamentos on bancos.codigo_pagamento = pagamentos.codigo_pagamento "
            where_clauses.append(f" and pagamentos.extraorcamentario = '{self.remove_break_lines(extraorcamentario)}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by bancos.nome_banco "
        order_by = " order by quantidade_pagamentos desc "
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
        df['nome'] = df['nome'].apply(self.insert_break_line)

        return df

    def get_dataframe_pagamentos_extraorcamentarios(self, banco: str = None) -> DataFrame:
        query_select = """
            select extraorcamentario as extra_orcamentario, 
                   count(*) as quantidade
        """

        query_from = """ 
            from despesas_pagamento pagamento
            inner join despesas_pagamento_lista_bancos bancos on pagamento.codigo_pagamento = bancos.codigo_pagamento
        """

        query_where = " where bancos.nome_banco is not null and bancos.nome_banco != '' "
        where_clauses = []

        if banco is not None:
            where_clauses.append(f" and bancos.nome_banco = '{self.remove_break_lines(banco)}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by extra_orcamentario "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
        """

        return self.helper.get_dataframe(query)

    def get_dataframe_valor_pagamentos_por_tempo(self, banco: str = None, extraorcamentario: str = None) -> DataFrame:
        query_select = """
            select pagamento.data_emissao as data, 
            sum(pagamento.valor_do_pagamento_convertido_pra_r) as valor
        """

        query_from = """ 
            from despesas_pagamento pagamento
        """

        query_where = " where 1=1 "
        where_clauses = []

        if banco is not None:
            query_from += " inner join despesas_pagamento_lista_bancos bancos on pagamento.codigo_pagamento = bancos.codigo_pagamento "
            where_clauses.append(f" and bancos.nome_banco = '{self.remove_break_lines(banco)}' ")

        if extraorcamentario is not None:
            where_clauses.append(f" and pagamento.extraorcamentario = '{self.remove_break_lines(extraorcamentario)}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by pagamento.data "
        order_by = " order by pagamento.data "

        query = f"""
            {query_select}
            {query_from}
            {query_where}
            {query_group_by}
            {order_by}
        """

        return self.helper.get_dataframe(query)

    def get_dataframe_quantidade_pagamentos_por_tempo(self, banco: str = None, extraorcamentario: str = None) -> DataFrame:
        query_select = """
               select pagamento.data_emissao as data, 
               count(pagamento.codigo_pagamento) as quantidade
           """

        query_from = """ 
           from despesas_pagamento pagamento
       """

        query_where = " where 1=1 "
        where_clauses = []

        if banco is not None:
            query_from += " inner join despesas_pagamento_lista_bancos bancos on pagamento.codigo_pagamento = bancos.codigo_pagamento "
            where_clauses.append(f" and bancos.nome_banco = '{self.remove_break_lines(banco)}' ")

        if extraorcamentario is not None:
            where_clauses.append(f" and pagamento.extraorcamentario = '{self.remove_break_lines(extraorcamentario)}' ")

        if len(where_clauses) > 0:
            query_where += " ".join(where_clauses)

        query_group_by = " group by pagamento.data "
        order_by = " order by pagamento.data "

        query = f"""
               {query_select}
               {query_from}
               {query_where}
               {query_group_by}
               {order_by}
           """

        return self.helper.get_dataframe(query)