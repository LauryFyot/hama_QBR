import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from layout import overview, baisse, risque

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # pour déploiement

sidebar = html.Div([
    html.H4("Analyse Sell-Out", className="text-white p-3"),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Overview", href="/", active="exact"),
        dbc.NavLink("Produits en baisse", href="/baisse", active="exact"),
        dbc.NavLink("Cas à risque", href="/risque", active="exact"),
    ], vertical=True, pills=True, className="p-2")
], style={"position": "fixed", "top": 0, "left": 0, "bottom": 0,
          "width": "18rem", "backgroundColor": "#2c3e50", "color": "white"})

content = html.Div(id="page-content", style={"marginLeft": "19rem", "marginRight": "2rem", "padding": "2rem 1rem"})

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/baisse":
        return baisse.layout
    elif pathname == "/risque":
        return risque.layout
    else:
        return overview.layout

if __name__ == "__main__":
    app.run(debug=True)
