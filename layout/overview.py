from dash import html, dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/all_data.csv", dtype={"AI summary": str, "EAN": str})
df['extract_date'] = pd.to_datetime(df['extract_date'], format='%Y-%m')
df['extract_date_str'] = df['extract_date'].dt.to_period("M").astype(str)

# Graphiques
sellout_total = df.groupby('extract_date_str')['COGS'].sum().reset_index()
fig1 = px.line(sellout_total, x='extract_date_str', y='COGS', title='Sell-out Total (COGS)')

# Évolution des unités vendues totales par mois
units_total = df.groupby('extract_date_str')['Unités'].sum().reset_index()
fig_units = px.line(units_total, x='extract_date_str', y='Unités', title='Unités vendues totales par mois')

sellout_cat = df.groupby(['extract_date_str', 'Cat. 1'])['COGS'].sum().reset_index()
fig2 = px.line(sellout_cat, x='extract_date_str', y='COGS', color='Cat. 1', title='Sell-out par Catégorie')

layout = html.Div([
    html.H3("Vue d'ensemble"),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig_units),
    dcc.Graph(figure=fig2)
])


# from dash import html, dcc, Input, Output
# import pandas as pd
# import plotly.express as px
# from app import app

# # === Données
# df = pd.read_csv("data/all_data.csv", dtype={"AI summary": str, "EAN": str}, low_memory=False)
# df['extract_date'] = pd.to_datetime(df['extract_date'], format='%Y-%m')
# df['extract_date_str'] = df['extract_date'].dt.to_period("M").astype(str)

# # === Graphiques fixes
# sellout_total = df.groupby('extract_date_str')['COGS'].sum().reset_index()
# fig1 = px.line(sellout_total, x='extract_date_str', y='COGS', title='Sell-out Total (COGS)')

# units_total = df.groupby('extract_date_str')['Unités'].sum().reset_index()
# fig_units = px.line(units_total, x='extract_date_str', y='Unités', title='Unités vendues totales par mois')

# # === Layout avec dropdown pour catégorie dynamique
# layout = html.Div([
#     html.H3("Vue d'ensemble"),
#     dcc.Graph(figure=fig1),
#     dcc.Graph(figure=fig_units),

#     dcc.Dropdown(
#         id='cat-dropdown',
#         options=[
#             {'label': 'Cat. 1', 'value': 'Cat. 1'},
#             {'label': 'Cat. 2', 'value': 'Cat. 2'},
#             {'label': 'Cat. 3', 'value': 'Cat. 3'},
#             {'label': 'Cat. 4', 'value': 'Cat. 4'}
#         ],
#         value='Cat. 1',
#         clearable=False,
#         style={'width': '300px'}
#     ),

#     dcc.Graph(id='category-graph')
# ])

# # === Callback pour mettre à jour le graphe dynamique
# @app.callback(
#     Output('category-graph', 'figure'),
#     Input('cat-dropdown', 'value')
# )
# def update_graph(cat_col):
#     dff = df[df[cat_col].notna()]  # filtre les valeurs nulles
#     data = dff.groupby(['extract_date_str', cat_col])['COGS'].sum().reset_index()
#     fig = px.line(data, x='extract_date_str', y='COGS', color=cat_col,
#                   title=f"Sell-out par {cat_col}")
#     return fig