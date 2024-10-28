import plotly.express as px

from data.access_objects.liquidacoes import LiquidacoesDAO


def get_figure_top_5_subitens(liquidacao_dao: LiquidacoesDAO, unidade_gestora: str = None, favorecido: str = None):
    dataframe = liquidacao_dao.get_dataframe_top5_sub_itens(
        unidade_gestora=unidade_gestora,
        favorecido=favorecido
    )

    fig = px.bar(
        dataframe,
        title='Top 5 Sub Itens',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693'],
        x='subitem',
        y='valor',
        color='subitem'
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff',
        xaxis=dict(
            tickmode='array'
        )
    )

    return fig


def get_figure_top5_diferenca_empenho_liquidacao(liquidacao_dao: LiquidacoesDAO,
                                                 unidade_gestora: str = None,
                                                 subitem: str = None,
                                                 favorecido: str = None):
    dataframe = liquidacao_dao.get_dataframe_top5_diferenca_valor_empenho_liquidado(
        unidade_gestora=unidade_gestora,
        subitem=subitem,
        favorecido=favorecido
    )

    fig = px.bar(
        dataframe.melt(id_vars='subitem', value_vars=['Empenho', 'Liquidado'], var_name='Valores', value_name='Valor'),
        x='subitem',
        y='Valor',
        color='Valores',
        barmode='group',
        title='Diferença dos Valores de Empenho e Liquidação',
        color_discrete_sequence=['#a72626', '#267ea7']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff',
        xaxis=dict(
            tickmode='array'
        )
    )

    return fig


def get_figure_top5_undiades_gestoras_mais_liquidacoes(liquidacao_dao: LiquidacoesDAO, subitem: str = None, favorecido: str = None):
    dataframe = liquidacao_dao.get_dataframe_top5_unidades_gestoras(
        subitem=subitem,
        favorecido=favorecido
    )

    fig = px.pie(
        dataframe,
        values='quantidade_liquidacoes',
        names='unidade',
        title='Top 5 Unidades Gestoras com Mais Liquidações',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig


def get_figure_top5_mais_favorecidos(liquidacao_dao: LiquidacoesDAO, subitem: str = None, unidade_gestora: str = None):
    dataframe = liquidacao_dao.get_dataframe_top5_favorecidos(
        subitem=subitem,
        unidade_gestora=unidade_gestora
    )

    fig = px.bar(
        dataframe,
        title='Top 5 Mais Favorecidos',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693'],
        x='favorecido',
        y='valor',
        color='favorecido'
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff',
        xaxis=dict(
            tickmode='array'
        )
    )

    return fig