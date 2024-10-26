import locale

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, Input, Output

from data.data_access_objects import CategoriaDespesaDAO, TipoCreditoDAO
from data.sqlite_db_helper import SQLite3Helper

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

urls = {
    'despesas_empenho': 'https://drive.google.com/uc?id=1u5aoMhovKez_ObK8TB_dEHSU6sZPP-GU',
    'despesas_item_empenho': 'https://drive.google.com/uc?id=1WnaaWlQARsgnS8YZi_45Pgm8Mm1gf7Cm',
    'despesas_item_empenho_historico': 'https://drive.google.com/uc?id=1TT8EdeQLoJIId_y7g2CPZ2R2urdpJ08P',
    'despesas_liquidacao_empenho_impactados': 'https://drive.google.com/uc?id=1fhAMqCrJxECSyLDZAPQeWv5Pc3c47h1d',
    'despesas_liquidacao': 'https://drive.google.com/uc?id=1V--FHmKvBmANycb7gg4Wl0uNErTs6YaK',
    'despesas_pagamento_empenhos_impactados': 'https://drive.google.com/uc?id=1Pjh-GhhWc8GP3ZLfNnjvUn-LVKckhHHv',
    'despesas_pagamento_favorecidos_finais': 'https://drive.google.com/uc?id=1Lb_HdNp64fL6-k6IdBIg-qqgKD59B_NQ',
    'despesas_pagamento_lista_bancos': 'https://drive.google.com/uc?id=1jQnRubYjLDCDKqFtN8AdQ--RRkXgJtvo',
    'despesas_pagamento_lista_faturas': 'https://drive.google.com/uc?id=1uW7W3ItcJHkA-CHj4hqF7dCrzNgpafrH',
    'despesas_pagamento_lista_precatorios': 'https://drive.google.com/uc?id=1UU4F2vRu9wfwT1SeOReVLc-lviHZpNzs',
    'despesas_pagamento': 'https://drive.google.com/uc?id=1pAdBk3aA56BUz3Ze0_iRcpDWJhOXwJxL'
}

helper = SQLite3Helper(db_name='despesas')
helper.create_database(urls=urls)

categoria_despesa_dao = CategoriaDespesaDAO(helper)
tipo_credito_dao = TipoCreditoDAO(helper)

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
                            id={'type': 'grafico', 'index': 'valor-tipo-credito'},
                            figure=get_figure_tipo_credito(),
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
        return html.H1('Em Desenvolvimento 1')
    elif aba == 'tab-despesas-pagamento':
        return html.H1('Em Desenvolvimento 2')


@app.callback(
    [
        Output({'type': 'grafico', 'index': 'valor-tipo-credito'}, 'figure'),
        Output({'type': 'grafico', 'index': 'quantidade-categorias'}, 'figure'),
        Output({'type': 'grafico', 'index': 'valor-categoria-tempo'}, 'figure'),
    ],
    [
        Input({'type': 'grafico', 'index': 'quantidade-categorias'}, 'clickData'),
        Input({'type': 'grafico', 'index': 'valor-tipo-credito'}, 'clickData')
    ],
)
def atualizar_graficos(clickData_categoria, clickData_tipo_credito):
    categoria_clicada = clickData_categoria['points'][0]['label'] if clickData_categoria else None
    tipo_credito_clicado = clickData_tipo_credito['points'][0]['label'] if clickData_tipo_credito else None

    fig_valor_categoria_tempo_filtrado = get_figure_valor_categoria_tempo(categoria_clicada, tipo_credito_clicado)
    fig_tipo_credito_filtrado = get_figure_tipo_credito(categoria_clicada)
    fig_quantidade_categoria_filtrado = get_figure_quantidade_categoria(tipo_credito_clicado)

    return fig_tipo_credito_filtrado, fig_quantidade_categoria_filtrado, fig_valor_categoria_tempo_filtrado


def get_figure_quantidade_categoria(tipo_credito_clicado=None):
    fig_categoria = px.pie(
        categoria_despesa_dao.get_dataframe_quantidade_categorias(tipo_credito=tipo_credito_clicado),
        values='quantidade',
        names='categoria',
        title='Categoria de Despesas',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )
    return fig_categoria


def get_figure_tipo_credito(categoria_clicada=None):
    df_valor_tipo_credito_filtrado = tipo_credito_dao.get_dataframe_valores_tipo_credito(
        categoria_despesa=categoria_clicada
    )
    fig_tipo_credito_filtrado = px.bar(
        df_valor_tipo_credito_filtrado,
        title='Valor das Despesas por Tipo de Crédito',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26'],
        x='tipo',
        y='valor',
        color='tipo'
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )
    return fig_tipo_credito_filtrado


def get_figure_valor_categoria_tempo(categoria_clicada=None, tipo_credito_clicado=None):
    df_valor_categoria_tempo_filtrado = categoria_despesa_dao.get_dataframe_valor_categoria_tempo(
        categoria_despesa=categoria_clicada,
        tipo_credito=tipo_credito_clicado,
    )
    fig_valor_categoria_tempo_filtrado = px.line(
        data_frame=df_valor_categoria_tempo_filtrado,
        x='data',
        y='valor',
        color='categoria',
        title='Valor das Categorias de Despesas por Tempo',
        line_shape='linear',
        color_discrete_sequence=['#a72626', '#2aa726', '#267ea7', '#a79f26']
    ).update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ffffff',
        font_color='#ffffff'
    )
    return fig_valor_categoria_tempo_filtrado


if __name__ == '__main__':
    app.run_server(debug=True)
