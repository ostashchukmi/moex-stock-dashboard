from dash import Input, Output
from utils.db import load_clusters_desc


def register_callbacks(app):

    @app.callback(
            Output('stocks-table', 'data'),
            Input('ticker-input', 'value'),
            Input('sector-dropdown', 'value'),
            Input('cluster-dropdown', 'value')
    )

    def update_dashboard(ticker_value, sector_value, cluster_value):
        data_table = load_clusters_desc()
        
        data_table['cluster'] = (
            data_table['cluster']
            .astype(str)
            .map(
                {
                    '0': 'Умеренно рискованные акции',
                    '1': 'Защитные акции',
                    '2': 'Спекулятивные акции',
                    '3': 'Низколиквидные умеренные акции'
                }
            )
    )

        if ticker_value:
            data_table = data_table[
                data_table['ticker']
                .str.contains(ticker_value,
                              case=False,
                              na=False)
            ]

        if sector_value:
            data_table = data_table[
                data_table['sector'] == sector_value
            ]

        if cluster_value:
            data_table = data_table[
                data_table['cluster'] == cluster_value
            ]

        return data_table.to_dict('records')
