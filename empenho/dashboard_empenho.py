import locale

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

from data.access_objects.despesas import DespesaEmpenhoDAO
from data.access_objects.liquidacoes import LiquidacoesDAO
from data.sqlite_db_helper import SQLite3Helper
from empenho.figures import get_figure_quantidade_categoria, get_figure_quantidade_tipo_operacao, \
    get_figure_tipo_credito, get_figure_funcoes_maior_investimento, get_figure_valor_categoria_tempo

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
        html.Div(
            id='conteudo',
            style={
                'backgroundColor': '#2c2c2c',
                'color': '#ffffff',
            },
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
                            figure=get_figure_quantidade_categoria(despesa_empenho_dao),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'quantidade-tipo-operacao'},
                            figure=get_figure_quantidade_tipo_operacao(despesa_empenho_dao),
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
                            figure=get_figure_tipo_credito(despesa_empenho_dao),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'funcoes-maior-investimento'},
                            figure=get_figure_funcoes_maior_investimento(despesa_empenho_dao),
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
                            figure=get_figure_valor_categoria_tempo(despesa_empenho_dao)
                        )
                    ]
                )
            ]
        )
    ]
)


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
    categoria_clicada = click_data_categoria['points'][0]['label'] if click_data_categoria else None
    tipo_credito_clicado = click_data_tipo_credito['points'][0]['label'] if click_data_tipo_credito else None
    tipo_operacao_clicada = click_data_quantidade_tipo_operacao['points'][0]['label'] if click_data_quantidade_tipo_operacao else None
    funcao_maior_investimento_clicada = click_data_funcao_maior_investimento['points'][0]['label'] if click_data_funcao_maior_investimento else None

    fig_valor_categoria_tempo_filtrado = get_figure_valor_categoria_tempo(
        despesa_empenho_dao=despesa_empenho_dao,
        categoria_despesa=categoria_clicada,
        tipo_credito=tipo_credito_clicado,
        tipo_operacao=tipo_operacao_clicada,
        funcao=funcao_maior_investimento_clicada
    )

    fig_tipo_credito_filtrado = get_figure_tipo_credito(
        despesa_empenho_dao=despesa_empenho_dao,
        categoria_despesa=categoria_clicada,
        funcao=funcao_maior_investimento_clicada,
        tipo_operacao=tipo_operacao_clicada
    )

    fig_quantidade_categoria_filtrado = get_figure_quantidade_categoria(
        despesa_empenho_dao=despesa_empenho_dao,
        tipo_credito=tipo_credito_clicado,
        tipo_operacao=tipo_operacao_clicada,
        funcao=funcao_maior_investimento_clicada,
    )

    fig_quantidade_tipo_operacao_filtrado = get_figure_quantidade_tipo_operacao(
        despesa_empenho_dao=despesa_empenho_dao,
        categoria_despesa=categoria_clicada,
        tipo_credito=tipo_credito_clicado,
        funcao=funcao_maior_investimento_clicada
    )

    fig_funcao_maior_investimento_filtrado = get_figure_funcoes_maior_investimento(
        despesa_empenho_dao=despesa_empenho_dao,
        categoria_despesa=categoria_clicada,
        tipo_credito=tipo_credito_clicado,
        tipo_operacao=tipo_operacao_clicada
    )

    return (fig_tipo_credito_filtrado,
            fig_quantidade_categoria_filtrado,
            fig_valor_categoria_tempo_filtrado,
            fig_funcao_maior_investimento_filtrado,
            fig_quantidade_tipo_operacao_filtrado)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.41', port=8050)
