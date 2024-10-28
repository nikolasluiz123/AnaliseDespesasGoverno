import plotly.express as px

from data.access_objects.pagamentos import PagamentosDAO


def get_figure_top5_bancos(pagamentos_dao: PagamentosDAO, extraorcamentario: str = None):
    dataframe = pagamentos_dao.get_dataframe_top5_bancos_mais_utilizados(
        extraorcamentario=extraorcamentario
    )

    fig = px.pie(
        dataframe,
        values='quantidade_pagamentos',
        names='nome',
        title='Top 5 Bancos Mais Utilizados',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig

def get_figure_pagamentos_extra_orcamentarios(pagamentos_dao: PagamentosDAO, banco: str = None):
    dataframe = pagamentos_dao.get_dataframe_pagamentos_extraorcamentarios(
        banco=banco
    )

    fig = px.pie(
        dataframe,
        values='quantidade',
        names='extra_orcamentario',
        title='Pagamentos Extra Orçamentários',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig

def get_figure_valor_pagamentos_por_tempo(pagamentos_dao: PagamentosDAO, banco: str = None, extraorcamentario: str = None):
    dataframe = pagamentos_dao.get_dataframe_valor_pagamentos_por_tempo(
        banco=banco,
        extraorcamentario=extraorcamentario
    )

    fig = px.line(
        data_frame=dataframe,
        x='data',
        y='valor',
        title='Valor dos Pagamentos por Tempo',
        line_shape='linear',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig

def get_figure_quantidade_pagamentos_por_tempo(pagamentos_dao: PagamentosDAO, banco: str = None, extraorcamentario: str = None):
    dataframe = pagamentos_dao.get_dataframe_quantidade_pagamentos_por_tempo(
        banco=banco,
        extraorcamentario=extraorcamentario
    )

    fig = px.line(
        data_frame=dataframe,
        x='data',
        y='quantidade',
        title='Quantidade de Pagamentos por Tempo',
        line_shape='linear',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig