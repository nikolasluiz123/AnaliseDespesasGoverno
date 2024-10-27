import locale

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, Input, Output

from data.access_objects.despesas import DespesaEmpenhoDAO
from data.access_objects.liquidacoes import LiquidacoesDAO
from data.sqlite_db_helper import SQLite3Helper

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

urls = {
    'despesas_empenho': 'data/files/Despesas_Empenho.csv',
    'despesas_item_empenho': 'data/files/Despesas_ItemEmpenho.csv',
    'despesas_item_empenho_historico': 'data/files/Despesas_ItemEmpenhoHistorico.csv',
    'despesas_liquidacao_empenho_impactados': 'data/files/Despesas_Liquidacao_EmpenhosImpactados.csv',
    'despesas_liquidacao': 'data/files/Despesas_Liquidacao.csv',
    'despesas_pagamento_empenhos_impactados': 'data/files/Despesas_Pagamento_EmpenhosImpactados.csv',
    'despesas_pagamento_favorecidos_finais': 'data/files/Despesas_Pagamento_FavorecidosFinais.csv',
    'despesas_pagamento_lista_bancos': 'data/files/Despesas_Pagamento_ListaBancos.csv',
    'despesas_pagamento_lista_faturas': 'data/files/Despesas_Pagamento_ListaFaturas.csv',
    'despesas_pagamento_lista_precatorios': 'data/files/Despesas_Pagamento_ListaPrecatorios.csv',
    'despesas_pagamento': 'data/files/Despesas_Pagamento.csv'
}

helper = SQLite3Helper(db_name='despesas')
helper.create_database(urls=urls)

despesa_empenho_dao = DespesaEmpenhoDAO(helper)
liquidacao_dao = LiquidacoesDAO(helper)

app = dash.Dash(__name__, external_stylesheets=['assets/styles.css', dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

app.layout = html.Div(
    style={
        'backgroundColor': '#2c2c2c',
        'color': '#ffffff',
    },
    children=[
        dcc.Tabs(
            id='tabs-menu',
            value='tab-despesas-empenho',
            style={
                'backgroundColor': '#2c2c2c',
                'color': '#ffffff',
                'border': 'none'
            },
            children=[
                dcc.Tab(label='Despesas do Empenho', value='tab-despesas-empenho'),
                dcc.Tab(label='Despesas em Liquidação', value='tab-despesas-liquidacao'),
                dcc.Tab(label='Pagamento das Despesas', value='tab-despesas-pagamento'),
            ]
        ),
        html.Div(
            id='conteudo-abas',
            style={
                'backgroundColor': '#2c2c2c',
                'color': '#ffffff',
            }
        )
    ]
)


@app.callback(
    Output('conteudo-abas', 'children'),
    Input('tabs-menu', 'value')
)
def exibir_conteudo(aba):
    if aba == 'tab-despesas-empenho':
        return html.Div(
            children=[
                html.Div(
                    style={
                        'display': 'flex',
                        'width': '100%',
                        'height': '50%',
                    },
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'quantidade-categorias'},
                            figure=get_figure_quantidade_categoria(),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'quantidade-tipo-operacao'},
                            figure=get_figure_quantidade_tipo_operacao(),
                            style={
                                'width': '50%'
                            }
                        ),
                    ]
                ),
                html.Div(
                    style={
                        'display': 'flex',
                        'width': '100%',
                        'height': '50%',
                    },
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'valor-tipo-credito'},
                            figure=get_figure_tipo_credito(),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'funcoes-maior-investimento'},
                            figure=get_figure_funcoes_maior_investimento(),
                            style={
                                'width': '50%'
                            }
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'valor-categoria-tempo'},
                            figure=get_figure_valor_categoria_tempo()
                        )
                    ]
                )
            ]
        )
    elif aba == 'tab-despesas-liquidacao':
        return html.Div(
            children=[
                html.Div(
                    style={
                        'display': 'flex',
                    },
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5_unidades_gestoras_mais_liquidacoes'},
                            figure=get_figure_top5_undiades_gestoras_mais_liquidacoes(),
                            style={
                                'width': '50%'
                            }
                        ),
                    ]
                ),
                html.Div(
                    style={
                        'display': 'flex',
                    },
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5_favorecidos'},
                            figure=get_figure_top5_mais_favorecidos(),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5_subitens'},
                            figure=get_figure_top_5_subitens(),
                            style={
                                'width': '50%'
                            }
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top10_diferenca_empenho_liquidacao'},
                            figure=get_figure_top10_diferenca_empenho_liquidacao(),
                        )
                    ]
                )
                # html.Div(
                #     style={
                #         'width': '100%',
                #     },
                #     children=[
                #         dcc.Graph(
                #             id={'type': 'grafico', 'index': 'top5_unidades_gestoras_mais_liquidacoes'},
                #             figure=get_figure_top5_undiades_gestoras_mais_liquidacoes()
                #         ),
                #         dcc.Graph(
                #             id={'type': 'grafico', 'index': 'top5_favorecidos'},
                #             figure=get_figure_top5_mais_favorecidos(),
                #         ),
                #         dcc.Graph(
                #             id={'type': 'grafico', 'index': 'top5_subitens'},
                #             figure=get_figure_top_5_subitens(),
                #         ),
                #         dcc.Graph(
                #             id={'type': 'grafico', 'index': 'top10_diferenca_empenho_liquidacao'},
                #             figure=get_figure_top10_diferenca_empenho_liquidacao(),
                #         )
                #     ]
                # )
            ]
        )
    elif aba == 'tab-despesas-pagamento':
        return html.H1('Em Desenvolvimento 2')


@app.callback(
    [
        Output({'type': 'grafico', 'index': 'valor-tipo-credito'}, 'figure'),
        Output({'type': 'grafico', 'index': 'quantidade-categorias'}, 'figure'),
        Output({'type': 'grafico', 'index': 'valor-categoria-tempo'}, 'figure'),
        Output({'type': 'grafico', 'index': 'funcoes-maior-investimento'}, 'figure'),
        Output({'type': 'grafico', 'index': 'quantidade-tipo-operacao'}, 'figure')
    ],
    [
        Input({'type': 'grafico', 'index': 'quantidade-categorias'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'valor-tipo-credito'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'quantidade-tipo-operacao'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'funcoes-maior-investimento'}, 'clickData'),
    ],
)
def atualizar_graficos(click_data_categoria,
                       click_data_tipo_credito,
                       click_data_quantidade_tipo_operacao,
                       click_data_funcao_maior_investimento):

    return atualizar_graficos_empenho(click_data_categoria,
                                      click_data_funcao_maior_investimento,
                                      click_data_quantidade_tipo_operacao,
                                      click_data_tipo_credito)


def atualizar_graficos_empenho(click_data_categoria,
                               click_data_funcao_maior_investimento,
                               click_data_quantidade_tipo_operacao,
                               click_data_tipo_credito):
    categoria_clicada = click_data_categoria['points'][0]['label'] if click_data_categoria else None
    tipo_credito_clicado = click_data_tipo_credito['points'][0]['label'] if click_data_tipo_credito else None
    tipo_operacao_clicada = click_data_quantidade_tipo_operacao['points'][0]['label'] if click_data_quantidade_tipo_operacao else None
    funcao_maior_investimento_clicada = click_data_funcao_maior_investimento['points'][0]['label'] if click_data_funcao_maior_investimento else None

    fig_valor_categoria_tempo_filtrado = get_figure_valor_categoria_tempo(
        categoria_despesa=categoria_clicada,
        tipo_credito=tipo_credito_clicado,
        tipo_operacao=tipo_operacao_clicada,
        funcao=funcao_maior_investimento_clicada
    )

    fig_tipo_credito_filtrado = get_figure_tipo_credito(
        categoria_despesa=categoria_clicada,
        funcao=funcao_maior_investimento_clicada,
        tipo_operacao=tipo_operacao_clicada
    )

    fig_quantidade_categoria_filtrado = get_figure_quantidade_categoria(
        tipo_credito=tipo_credito_clicado,
        tipo_operacao=tipo_operacao_clicada,
        funcao=funcao_maior_investimento_clicada,
    )

    fig_quantidade_tipo_operacao_filtrado = get_figure_quantidade_tipo_operacao(categoria_despesa=categoria_clicada,
                                                                                tipo_credito=tipo_credito_clicado,
                                                                                funcao=funcao_maior_investimento_clicada)

    fig_funcao_maior_investimento_filtrado = get_figure_funcoes_maior_investimento(categoria_despesa=categoria_clicada,
                                                                                   tipo_credito=tipo_credito_clicado,
                                                                                   tipo_operacao=tipo_operacao_clicada)
    return (fig_tipo_credito_filtrado,
            fig_quantidade_categoria_filtrado,
            fig_valor_categoria_tempo_filtrado,
            fig_funcao_maior_investimento_filtrado,
            fig_quantidade_tipo_operacao_filtrado)


def get_figure_quantidade_categoria(
        tipo_credito=None,
        tipo_operacao=None,
        funcao=None,
):
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


def get_figure_quantidade_tipo_operacao(categoria_despesa: str = None,
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


def get_figure_tipo_credito(
        categoria_despesa=None,
        funcao=None,
        tipo_operacao=None
):
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


def get_figure_funcoes_maior_investimento(
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


def get_figure_valor_categoria_tempo(
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


def get_figure_top5_mais_favorecidos(subitem: str = None, unidade_gestora: str = None):
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


def get_figure_top_5_subitens(unidade_gestora: str = None):
    dataframe = liquidacao_dao.get_dataframe_top5_sub_itens(
        unidade_gestora=unidade_gestora
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


def get_figure_top10_diferenca_empenho_liquidacao(unidade_gestora: str = None, subitem: str = None):
    dataframe = liquidacao_dao.get_dataframe_top10_diferenca_valor_empenho_liquidado(
        unidade_gestora=unidade_gestora,
        subitem=subitem
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


def get_figure_top5_undiades_gestoras_mais_liquidacoes(subitem: str = None):
    dataframe = liquidacao_dao.get_dataframe_top5_unidades_gestoras(
        subitem=subitem,
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


if __name__ == '__main__':
    app.run_server(debug=True)
