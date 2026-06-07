from dash import Dash
import dash_bootstrap_components as dbc
from layouts import create_layout
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Исследование закономерностей поведения рынка акций Московской биржи'
app.layout = create_layout()
server = app.server

register_callbacks(app)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8050,
        debug=False,
    )
