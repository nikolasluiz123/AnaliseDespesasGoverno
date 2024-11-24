import locale

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input

from data.access_objects.liquidacoes import LiquidacoesDAO
from data.sqlite_db_helper import SQLite3Helper
from liquidacao.figures import get_figure_top5_diferenca_empenho_liquidacao, get_figure_top_5_subitens, \
    get_figure_top5_mais_favorecidos, get_figure_top5_undiades_gestoras_mais_liquidacoes

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

helper = SQLite3Helper(db_name='despesas')
helper.create_database()

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
                    },
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5-unidades-gestoras-mais-liquidacoes'},
                            figure=get_figure_top5_undiades_gestoras_mais_liquidacoes(liquidacao_dao),
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
                            id={'type': 'grafico', 'index': 'top5-favorecidos'},
                            figure=get_figure_top5_mais_favorecidos(liquidacao_dao),
                            style={
                                'width': '50%'
                            }
                        ),
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5-subitens'},
                            figure=get_figure_top_5_subitens(liquidacao_dao),
                            style={
                                'width': '50%'
                            }
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id={'type': 'grafico', 'index': 'top5-diferenca-empenho-liquidacao'},
                            figure=get_figure_top5_diferenca_empenho_liquidacao(liquidacao_dao),
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output({'type': 'grafico', 'index': 'top5-unidades-gestoras-mais-liquidacoes'}, 'figure'),
        Output({'type': 'grafico', 'index': 'top5-favorecidos'}, 'figure'),
        Output({'type': 'grafico', 'index': 'top5-subitens'}, 'figure'),
        Output({'type': 'grafico', 'index': 'top5-diferenca-empenho-liquidacao'}, 'figure'),
    ],
    [
        Input({'type': 'grafico', 'index': 'top5-unidades-gestoras-mais-liquidacoes'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'top5-favorecidos'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'top5-subitens'}, 'clickData'),
    ],
)
def atualizar_graficos(click_data_unidade_gestora,
                       click_data_favorecidos,
                       click_data_subitem):
    unidade_gestora_clicada = click_data_unidade_gestora['points'][0]['label'] if click_data_unidade_gestora else None
    favorecido_clicado = click_data_favorecidos['points'][0]['label'] if click_data_favorecidos else None
    subitem_clicado = click_data_subitem['points'][0]['label'] if click_data_subitem else None

    fig_top5_undiades_gestoras_mais_liquidacoes = get_figure_top5_undiades_gestoras_mais_liquidacoes(
        liquidacao_dao=liquidacao_dao,
        subitem=subitem_clicado,
        favorecido=favorecido_clicado
    )

    fig_top5_mais_favorecidos = get_figure_top5_mais_favorecidos(liquidacao_dao=liquidacao_dao,
                                                                 subitem=subitem_clicado,
                                                                 unidade_gestora=unidade_gestora_clicada)

    fig_top_5_subitens = get_figure_top_5_subitens(liquidacao_dao=liquidacao_dao,
                                                   unidade_gestora=unidade_gestora_clicada,
                                                   favorecido=favorecido_clicado)

    fig_top5_diferenca_empenho_liquidacao = get_figure_top5_diferenca_empenho_liquidacao(
        liquidacao_dao=liquidacao_dao,
        subitem=subitem_clicado,
        unidade_gestora=unidade_gestora_clicada,
        favorecido=favorecido_clicado
    )

    return (fig_top5_undiades_gestoras_mais_liquidacoes,
            fig_top5_mais_favorecidos,
            fig_top_5_subitens,
            fig_top5_diferenca_empenho_liquidacao)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8051)
