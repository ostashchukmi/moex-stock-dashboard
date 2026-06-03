import warnings

import numpy as np
import pandas as pd

import requests

from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

warnings.filterwarnings("ignore")

from utils.db import engine

stock_url = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities.json'

stock_desc_response = requests.get(stock_url).json()

columns = stock_desc_response['securities']['columns']
data = stock_desc_response['securities']['data']

stock_desc_data = pd.DataFrame(data, columns=columns)

stock_desc_data = stock_desc_data[(stock_desc_data['BOARDID'] == 'TQBR') & (stock_desc_data['STATUS'] == 'A')]

tickers = stock_desc_data['SECID'].unique()

history = []

for ticker in tickers:
    url_history = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json'

    params = {
    'from': '2022-05-01',
    'till': '2023-05-01',
    'interval': 24
    }
    response_history = requests.get(url_history, params=params).json()

    columns = response_history['candles']['columns']
    data = response_history['candles']['data']
    ticker_df = pd.DataFrame(data, columns=columns)
    ticker_df['ticker'] = ticker

    history.append(ticker_df)

history_22_23 = pd.concat(history, ignore_index=True)

history = []

for ticker in tickers:
    url_history = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json'

    params = {
    'from': '2023-05-01',
    'till': '2024-05-01',
    'interval': 24
    }
    response_history = requests.get(url_history, params=params).json()

    columns = response_history['candles']['columns']
    data = response_history['candles']['data']
    ticker_df = pd.DataFrame(data, columns=columns)
    ticker_df['ticker'] = ticker

    history.append(ticker_df)

history_23_24 = pd.concat(history, ignore_index=True)

history = []

for ticker in tickers:
    url_history = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json'

    params = {
    'from': '2024-05-01',
    'till': '2025-05-01',
    'interval': 24
    }
    response_history = requests.get(url_history, params=params).json()

    columns = response_history['candles']['columns']
    data = response_history['candles']['data']
    ticker_df = pd.DataFrame(data, columns=columns)
    ticker_df['ticker'] = ticker

    history.append(ticker_df)

history_24_25 = pd.concat(history, ignore_index=True)

history = []

for ticker in tickers:
    url_history = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json'

    params = {
    'from': '2025-05-01',
    'till': '2026-05-01',
    'interval': 24
    }
    response_history = requests.get(url_history, params=params).json()

    columns = response_history['candles']['columns']
    data = response_history['candles']['data']
    ticker_df = pd.DataFrame(data, columns=columns)
    ticker_df['ticker'] = ticker

    history.append(ticker_df)

history_25_26 = pd.concat(history, ignore_index=True)

all_tickets_history = pd.concat([history_22_23, history_23_24, history_24_25, history_25_26], ignore_index=True)

dictionary = pd.read_excel('dictionary.xlsx')

history = all_tickets_history[['ticker', 'begin', 'close', 'value']]
history = history.sort_values(['ticker', 'begin'])
history['begin'] = pd.to_datetime(history['begin'])
history = history[
(history['ticker'] != 'BTBR') &
(history['ticker'] != 'GAZC') &
(history['ticker'] != 'GAZS') &
(history['ticker'] != 'GAZT') ]
history['return'] = (history.groupby('ticker')['close'].pct_change())

history_agg = history.groupby('ticker').agg({'return': ['mean', 'std'], 'value': 'mean'}).reset_index()
history_agg.columns = ['ticker', 'mean_return', 'volatility', 'mean_value']
history_agg['mean_value_log'] = np.log1p(history_agg['mean_value'])

X = history_agg[['mean_return', 'volatility', 'mean_value_log']]
X = StandardScaler().fit_transform(X)

model_kmeans = KMeans(
    n_clusters=4,
    init='k-means++',
    n_init='auto',
    random_state=1,
    verbose=1
)

model_kmeans.fit(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

clusters = pd.DataFrame(
    X,
    columns=[
        'mean_return',
        'volatility',
        'mean_value_log'
    ]
)
clusters['cluster'] = model_kmeans.labels_

clusters_heatmap = clusters.groupby('cluster')[['mean_return', 'volatility', 'mean_value_log']].mean()
clusters_heatmap = clusters_heatmap.reset_index()

clusters_desc = history_agg.copy()
clusters_desc['cluster'] = model_kmeans.labels_
clusters_desc['pca1'] = X_pca[:, 0]
clusters_desc['pca2'] = X_pca[:, 1]
clusters_desc['return_scaled'] = X[:, 0]
clusters_desc['volatility_scaled'] = X[:, 1]
clusters_desc['liquidity_scaled'] = X[:, 2]
clusters_desc = clusters_desc.merge(dictionary, how='left', on='ticker')

clusters_sectors = clusters_desc.groupby(['sector', 'cluster'])['isin'].count().reset_index().rename(columns={'isin': 'count'})
clusters_sectors['id'] = range(1, len(clusters_sectors) + 1)
clusters_sectors = clusters_sectors[['id', 'sector', 'cluster', 'count']]

clusters_desc.to_sql(
    'clusters_desc',
    engine,
    if_exists='replace',
    index=False,
)

clusters_heatmap.to_sql(
    'clusters_heatmap',
    engine,
    if_exists='replace',
    index=False,
)

clusters_sectors.to_sql(
    'clusters_sectors',
    engine,
    if_exists='replace',
    index=False,
)
