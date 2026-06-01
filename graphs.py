from dash import dash_table
from utils.db import load_clusters_heatmap, load_clusters_desc, load_clusters_sectors
import plotly.express as px


def load_scatter():

    clusters_desc = load_clusters_desc()

    clusters_desc['cluster'] = (
    clusters_desc['cluster']
    .astype(str)
    .map({
        '0': 'Умеренно рискованные акции ',
        '1': 'Защитные акции',
        '2': 'Спекулятивные акции',
        '3': 'Низколиквидные умеренные акции'
    })
    )

    fig = px.scatter(
        clusters_desc,

        x='pca1',
        y='pca2',

        color='cluster',
        color_discrete_map={
        'Умеренно рискованные акции ': '#FFA343',
        'Защитные акции': '#008000',
        'Спекулятивные акции': '#800080',
        'Низколиквидные умеренные акции': '#42AAFF'
        },

        hover_data={
            'cluster': False,
            'pca1': False,
            'pca2': False,
            'ticker': True,
            'sector': True,
            'mean_return': True,
            'mean_value': ':.2f',
            'volatility': ':.2f'
            },

        labels={
            'ticker': 'Тикер',
            'sector': 'Сектор',
            'mean_return': 'Средняя доходность',
            'mean_value': 'Средняя ликвидность',
            'volatility': 'Средняя волатильность',
            'cluster': 'Кластер'
            },

        text='ticker',

        title='Кластеры акций Московской биржи (метод k-средних)'
    )

    fig.update_traces(
    textfont_size=6
    )

    fig.update_xaxes(
    showticklabels=False
    )

    fig.update_yaxes(
    showticklabels=False
    )
    
    fig.update_layout(

    font = {'family': 'Mulish'},

    title_x=0.5,

    title_font=dict(
        color='black',
        size=16
    ),

    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5
        ),

    legend_title_text='',

    legend_font=dict(
        color='black'
    ),

    xaxis_title=None,

    yaxis_title=None
    )

    return fig


def load_heatmap():
    clusters_heatmap = load_clusters_heatmap()
    clusters_heatmap = (
        clusters_heatmap
        .set_index('cluster')
        .round(1)
    )

    clusters_heatmap.columns = [
        'Доходность',
        'Волатильность',
        'Ликвидность'
        ]

    clusters_heatmap.index = [
        'Умеренно рискованные акции',
        'Защитные акции',
        'Спекулятивные акции',
        'Низколиквидные умеренные акции'
        ]

    fig = px.imshow(
        clusters_heatmap,
        text_auto=True,
        color_continuous_scale='RdBu',
        aspect='auto',
        title='Параметры кластеров по стандартизированным признакам',
    )

    fig.update_xaxes(
        tickfont=dict(
        color='black'
        )
        )

    fig.update_yaxes(
        tickfont=dict(
        color='black'
        )
        )

    fig.update_layout(
        font = {'family': 'Mulish'},
        title_x=0.5,
        coloraxis_showscale=False,
        title_font=dict(
        color='black',
        size=16
        ),
     
        height=400,

        xaxis_title=None,
        yaxis_title=None,
        )

    return fig


def load_treemap():
    clusters_sectors = load_clusters_sectors()
    clusters_sectors['cluster'] = (
        clusters_sectors['cluster']
        .astype(str)
        .map({
            '0': 'Умеренно рискованные акции ',
            '1': 'Защитные акции',
            '2': 'Спекулятивные акции',
            '3': 'Низколиквидные умеренные акции'
            })
        )

    fig = px.treemap(
        clusters_sectors,
        path=['cluster', 'sector'],
        values='count',
        color='cluster',
        color_discrete_map={
        'Умеренно рискованные акции ': '#FFA343',
        'Защитные акции': '#008000',
        'Спекулятивные акции': '#800080',
        'Низколиквидные умеренные акции': '#42AAFF'
        }
    )

    fig.update_traces(
       textinfo='label+value',
       
       hoverinfo='skip',
       
       hovertemplate=None
   )

    fig.update_layout(
        font = {'family': 'Mulish'},
        title='Распределение отраслей внутри кластеров',
        title_x=0.5,
        
        title_font=dict(
        color='black',
        size=16
        ),
                
        height=400,
        )
    return fig


def load_barchart():
    clusters_sectors = load_clusters_sectors()
    clusters_sectors = clusters_sectors.sort_values(
    by=['cluster', 'count'],
    ascending=[True, False]
    )

    clusters_sectors['cluster'] = (
    clusters_sectors['cluster']
    .astype(str)
    .map({
        '0': 'Умеренно рискованные акции',
        '1': 'Защитные акции',
        '2': 'Спекулятивные акции',
        '3': 'Низколиквидные умеренные акции'
    })
    )

    fig = px.bar(
        clusters_sectors,
        x='sector',
        y='count',
        color='cluster',
        color_discrete_map={
        'Умеренно рискованные акции': '#FFA343',
        'Защитные акции': '#008000',
        'Спекулятивные акции': '#800080',
        'Низколиквидные умеренные акции': '#42AAFF'
        },

        barmode='stack',
        text='count',

        labels={
            'sector': 'Сектор',
            'count': 'Количество акций',
            'cluster': 'Кластер'
        },

        title='Распределение кластеров по отраслям'
    )

    fig.update_traces(
    textfont_size=10,
    textposition='inside',
    textangle=0

    )

    fig.update_yaxes(
    showticklabels=False
    )

    fig.update_xaxes(
        tickfont=dict(
        color='black'
        )
        )

    fig.update_layout(
    font = {'family': 'Mulish'},

    title_x=0.5,

    title_font=dict(
        color='black',
        size=16
    ),

    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5
        ),

    legend_title_text='',

    legend_font=dict(
        color='black'
    ),

    xaxis_title=None,

    yaxis_title=None
    )

    return fig


def load_table():
    clusters_desc = load_clusters_desc()
    clusters_desc['mean_return'] = (
        clusters_desc['mean_return']
        .round(2)
    )

    clusters_desc['mean_value'] = (
        clusters_desc['mean_value']
        .round(2)
    )

    clusters_desc['volatility'] = (
        clusters_desc['volatility']
        .round(2)
    )

    table = dash_table.DataTable(

        id='stocks-table',
        data=clusters_desc.to_dict('records'),
       columns=[
            {
                "name": "Тикер",
                "id": "ticker"
            },

            {
                "name": "Описание",
                "id": "description"
            }
        ],
        page_size=15,
        style_cell={
            'textAlign': 'left',
            'fontFamily': 'Mulish',
            'fontSize': '14px',
            'color': '#2c2c2c'
        },

        style_header={
        'fontFamily': 'Mulish',
        'fontWeight': '700',
        'fontSize': '15px'
        },

        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },

        style_table={
            'overflowX': 'auto'
        }
    )

    return table
