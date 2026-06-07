import dash_bootstrap_components as dbc
from dash import dcc, html

from graphs import load_heatmap, load_scatter, load_barchart, load_treemap, load_table
from utils.db import load_clusters_desc

CLUSTER_NAMES = {
    '0': 'Умеренно рискованные акции',
    '1': 'Защитные акции',
    '2': 'Спекулятивные акции',
    '3': 'Низколиквидные умеренные акции',
}


def create_layout():
    clusters_desc = load_clusters_desc()
    clusters_desc['cluster'] = (
        clusters_desc['cluster']
        .astype(str)
        .map(CLUSTER_NAMES)
    )

    sector_options = [
        {
            'label': sector,
            'value': sector,
        }
        for sector in sorted(
            clusters_desc['sector'].dropna().unique()
        )
    ]

    cluster_options = [
        {
            'label': cluster,
            'value': cluster,
        }
        for cluster in sorted(
            clusters_desc['cluster'].dropna().unique()
        )
    ]

    return dbc.Container(
        [
            dbc.NavbarSimple(
                brand='Исследование закономерностей поведения рынка акций Московской биржи',
                className='custom-navbar',
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(
                            label='Общая картина рынка',
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=load_scatter(),
                                                style={
                                                    'height': '650px'
                                                    }
                                            ),
                                            width=8,
                                            xs=12,
                                            md=8,
                                            className='custom-card mb-3 mt-3',
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Graph(
                                                    figure=load_heatmap(),
                                                    style={
                                                        'height': '325px'
                                                    }
                                                ),
                                                dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                            html.P('Умеренно рискованные акции.',
                                                                   className='cluster-title-0',
                                                                ),
                                                            html.P('''
                                                                   Доходность немного выше средней. 
                                                                   Акции имеют повышенный, но не экстремальный риск.
                                                                   Ликвидность близка к среднерыночной.
                                                                   ''',
                                                                   className='info-text',
                                                                ),
                                                            html.P('Защитные акции.',
                                                                   className='cluster-title-1',
                                                                ),
                                                            html.P('''
                                                                   Доходность заметно ниже средней.
                                                                   Риск ниже среднего – низкая волатильность.
                                                                   Бумаги активно торгуются, имеют высокий спрос.
                                                                   ''',
                                                                   className='info-text',
                                                                ),
                                                            html.P('Спекулятивные акции.',
                                                                   className='cluster-title-2',
                                                                ),
                                                            html.P('''
                                                                   Доходность очень высокая.
                                                                   Сильные колебания цен, высокий риск.
                                                                   Акции торгуются менее активно.
                                                                   ''',
                                                                   className='info-text',
                                                                ),
                                                            html.P('Низколиквидные умеренные акции.',
                                                                   className='cluster-title-3',
                                                                ),
                                                            html.P('''
                                                                   Доходность близка к среднерыночной.
                                                                   Колебания цен чуть спокойнее рынка.
                                                                   Менее популярны у участников рынка.
                                                                   ''',
                                                                   className='info-text',
                                                                   )
                                                        ]
                                                    ),
                                                    className='info-card mb-3',
                                                ),
                                            ],
                                            width=4,
                                            xs=12,
                                            md=4,
                                            className='custom-card mb-3 mt-3',
                                        ),
                                    ],
                                    className='px-3',
                                ),
                                dbc.Row(
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=load_treemap(),
                                                style={
                                                    'height': '700px',
                                                    }
                                                ),
                                                width=12,
                                                xs=12,
                                                md=12,
                                                className='custom-card mb-3 mt-3',
                                        ),
                                        className='px-3',
                                ),
                            ]
                        ),
                        dbc.Tab(
                            label='Отраслевой анализ',
                            children=[
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=load_barchart(),
                                            style={
                                                'height': '600px'
                                            }
                                        ),
                                        width=12,
                                        xs=12,
                                        md=12,
                                        className='custom-card mb-3 mt-3',
                                    ),
                                    className='px-3',
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Input(
                                                id='ticker-input',
                                                placeholder='Введите тикер акции',
                                                type='text',
                                            ),
                                            width=4,
                                            xs=12,
                                            md=4,
                                            className='custom-card mb-3 mt-3',
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='sector-dropdown',
                                                placeholder='Выберите отрасль',
                                                searchable=False,
                                                options=sector_options,
                                            ),
                                            width=4,
                                            className='custom-card mb-3 mt-3',
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='cluster-dropdown',
                                                placeholder='Выберите кластер',
                                                searchable=False,
                                                options=cluster_options,
                                            ),
                                            className='custom-card mb-3 mt-3',
                                        )
                                    ],
                                    className='px-3',
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        load_table(),
                                        width=12,
                                        className='custom-card mb-3 mt-3',
                                    ),
                                    className='px-3',
                                )
                            ]
                        )
                    ],
                    className='custom-tabs',
                ),
            ],
            fluid=True
        )
