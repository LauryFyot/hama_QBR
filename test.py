import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Données d'exemple
df = pd.read_csv("data/all_data.csv", low_memory=False)
df['extract_date_str'] = pd.to_datetime(df['extract_date'], format='%Y-%m').dt.to_period("M").astype(str)

# App Dash simple
app = Dash(__name__)

app.layout = html.Div([
    html.H3("Catégorie dynamique"),
    
    dcc.Dropdown(
        id='cat-dropdown',
        options=[
            {'label': 'Cat. 1', 'value': 'Cat. 1'},
            {'label': 'Cat. 2', 'value': 'Cat. 2'},
            {'label': 'Cat. 3', 'value': 'Cat. 3'},
            {'label': 'Cat. 4', 'value': 'Cat. 4'}
        ],
        value='Cat. 1',
        clearable=False,
        style={'width': '300px'}
    ),

    dcc.Graph(id='category-graph')
])

@app.callback(
    Output('category-graph', 'figure'),
    Input('cat-dropdown', 'value')
)
def update_graph(cat_col):
    dff = df[df[cat_col].notna()]  # filtre les valeurs nulles
    data = dff.groupby(['extract_date_str', cat_col])['COGS'].sum().reset_index()
    fig = px.line(data, x='extract_date_str', y='COGS', color=cat_col,
                  title=f"Sell-out par {cat_col}")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
