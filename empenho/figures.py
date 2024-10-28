import plotly.express as px

from data.access_objects.despesas import DespesaEmpenhoDAO


def get_figure_quantidade_categoria(despesa_empenho_dao: DespesaEmpenhoDAO,
                                    tipo_credito=None,
                                    tipo_operacao=None,
                                    funcao=None):
    dataframe = despesa_empenho_dao.get_dataframe_quantidade_categorias(
        tipo_credito=tipo_credito,
        tipo_operacao=tipo_operacao,
        funcao=funcao
    )

    fig = px.pie(
        dataframe,
        values='quantidade',
        names='categoria',
        title='Categoria de Despesas',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )
    return fig


def get_figure_quantidade_tipo_operacao(despesa_empenho_dao: DespesaEmpenhoDAO,
                                        categoria_despesa: str = None,
                                        tipo_credito: str = None,
                                        funcao: str = None):
    dataframe = despesa_empenho_dao.get_dataframe_quantidade_tipo_operacao(
        categoria_despesa=categoria_despesa,
        tipo_credito=tipo_credito,
        funcao=funcao
    )

    fig = px.pie(
        dataframe,
        values='quantidade',
        names='tipo',
        title='Tipos de Operação',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig


def get_figure_tipo_credito(despesa_empenho_dao: DespesaEmpenhoDAO,
                            categoria_despesa=None,
                            funcao=None,
                            tipo_operacao=None):
    dataframe = despesa_empenho_dao.get_dataframe_valores_tipo_credito(
        categoria_despesa=categoria_despesa,
        funcao=funcao,
        tipo_operacao=tipo_operacao
    )

    fig = px.bar(
        dataframe,
        title='Tipos de Crédito',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693'],
        x='tipo',
        y='valor',
        color='tipo'
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig


def get_figure_funcoes_maior_investimento(despesa_empenho_dao: DespesaEmpenhoDAO,
                                          categoria_despesa: str = None,
                                          tipo_credito: str = None,
                                          tipo_operacao: str = None
                                          ):
    dataframe = despesa_empenho_dao.get_dataframe_top5_funcoes_maior_investimento(
        categoria_despesa=categoria_despesa,
        tipo_credito=tipo_credito,
        tipo_operacao=tipo_operacao
    )

    fig = px.bar(
        dataframe,
        title='Top 5 Funções com Maior Investimento',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693'],
        x='funcao',
        y='valor',
        color='funcao'
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig


def get_figure_valor_categoria_tempo(despesa_empenho_dao: DespesaEmpenhoDAO,
                                     categoria_despesa=None,
                                     tipo_credito=None,
                                     tipo_operacao=None,
                                     funcao=None
                                     ):
    dataframe = despesa_empenho_dao.get_dataframe_valor_categoria_tempo(
        categoria_despesa=categoria_despesa,
        tipo_credito=tipo_credito,
        tipo_operacao=tipo_operacao,
        funcao=funcao
    )

    fig = px.line(
        data_frame=dataframe,
        x='data',
        y='valor',
        color='categoria',
        title='Despesas por Categoria',
        line_shape='linear',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26', '#a76326', '#5b26a7', '#a72693']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )

    return fig
