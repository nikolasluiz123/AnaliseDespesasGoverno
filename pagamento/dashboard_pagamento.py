import locale

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input

from data.access_objects.pagamentos import PagamentosDAO
from data.sqlite_db_helper import SQLite3Helper
from pagamento.figures import get_figure_top5_bancos, get_figure_pagamentos_extra_orcamentarios, \
    get_figure_valor_pagamentos_por_tempo, get_figure_quantidade_pagamentos_por_tempo

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

pagamento_dao = PagamentosDAO(helper)

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
                    },
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5-bancos'},
                            figure=get_figure_top5_bancos(pagamento_dao),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'extra_orcamentario'},
                            figure=get_figure_pagamentos_extra_orcamentarios(pagamento_dao),
                            style={
                                'width': '50%'
                            }
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'valor-pagamentos-por-tempo'},
                            figure=get_figure_valor_pagamentos_por_tempo(pagamento_dao)
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'quantidade-pagamentos-por-tempo'},
                            figure=get_figure_quantidade_pagamentos_por_tempo(pagamento_dao)
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output({'type': 'grafico', 'index': 'top5-bancos'}, 'figure'),
        Output({'type': 'grafico', 'index': 'extra_orcamentario'}, 'figure'),
        Output({'type': 'grafico', 'index': 'valor-pagamentos-por-tempo'}, 'figure'),
        Output({'type': 'grafico', 'index': 'quantidade-pagamentos-por-tempo'}, 'figure'),
    ],
    [
        Input({'type': 'grafico', 'index': 'top5-bancos'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'extra_orcamentario'}, 'clickData'),
    ],
)
def atualizar_graficos(click_data_bancos,
                       click_data_extra_orcamentario):
    banco_clicado = click_data_bancos['points'][0]['label'] if click_data_bancos else None
    extra_orcamentario_clicado = click_data_extra_orcamentario['points'][0]['label'] if click_data_extra_orcamentario else None

    fig_top5_bancos = get_figure_top5_bancos(pagamentos_dao=pagamento_dao, extraorcamentario=extra_orcamentario_clicado)

    fig_extra_orcamentarios = get_figure_pagamentos_extra_orcamentarios(pagamentos_dao=pagamento_dao,
                                                                        banco=banco_clicado)

    fig_valor_pagamentos_tempo = get_figure_valor_pagamentos_por_tempo(pagamentos_dao=pagamento_dao,
                                                                       banco=banco_clicado,
                                                                       extraorcamentario=extra_orcamentario_clicado)

    fig_quantidade_pagamentos_tempo = get_figure_quantidade_pagamentos_por_tempo(pagamentos_dao=pagamento_dao,
                                                                                 banco=banco_clicado,
                                                                                 extraorcamentario=extra_orcamentario_clicado)



    return fig_top5_bancos, fig_extra_orcamentarios, fig_valor_pagamentos_tempo, fig_quantidade_pagamentos_tempo


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.41', port=8052)
