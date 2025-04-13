from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
from app import app

# === Données

df = pd.read_csv("data/all_data.csv", dtype={"AI summary": str, "EAN": str}, low_memory=False)
df['extract_date'] = pd.to_datetime(df['extract_date'], format='%Y-%m').dt.to_period("M")

# === Préparation des données
pivot_cogs = df.pivot_table(index='ASIN', columns='extract_date', values='COGS', aggfunc='sum')

# Calculs des deltas
pivot_cogs['delta_dec'] = pivot_cogs[pd.Period("2024-12")] - pivot_cogs[pd.Period("2024-11")]
pivot_cogs['delta_jan'] = pivot_cogs[pd.Period("2025-01")] - pivot_cogs[pd.Period("2024-12")]
pivot_cogs['delta_feb'] = pivot_cogs[pd.Period("2025-02")] - pivot_cogs[pd.Period("2025-01")]
pivot_cogs['delta_mar'] = pivot_cogs[pd.Period("2025-03")] - pivot_cogs[pd.Period("2025-02")]

pivot_cogs['delta_dec_perc'] = pivot_cogs['delta_dec'] / pivot_cogs[pd.Period("2024-11")]
pivot_cogs['delta_jan_perc'] = pivot_cogs['delta_jan'] / pivot_cogs[pd.Period("2024-12")]
pivot_cogs['delta_feb_perc'] = pivot_cogs['delta_feb'] / pivot_cogs[pd.Period("2025-01")]
pivot_cogs['delta_mar_perc'] = pivot_cogs['delta_mar'] / pivot_cogs[pd.Period("2025-02")]

# Détection des baisses
pivot_cogs['baisse_detectée'] = (
    (pivot_cogs['delta_dec'] < -20) |
    (pivot_cogs['delta_jan'] < -20) |
    (pivot_cogs['delta_feb'] < -20) |
    (pivot_cogs['delta_mar'] < -20)
)

# Fusion avec les noms produits
produits_baisse = pivot_cogs[pivot_cogs['baisse_detectée']].sort_values(by='delta_mar')
noms = df[['ASIN', 'Nom du produit']].drop_duplicates()
produits_baisse = produits_baisse.reset_index().merge(noms, on='ASIN', how='left')

# === Layout Dash avec tableau
layout = html.Div([
    html.H3("Produits en baisse de sell-out"),
    html.P("Liste des produits ayant subi une baisse significative (>20€) sur un des derniers mois."),

    dash_table.DataTable(
        columns=[
            {"name": col, "id": col} for col in ['ASIN', 'Nom du produit', '2024-11', '2024-12', '2025-01', '2025-02', '2025-03',
                                                  'delta_dec', 'delta_jan', 'delta_feb', 'delta_mar']
            if col in produits_baisse.columns
        ],
        data=produits_baisse.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={"textAlign": "left", 'minWidth': '120px', 'whiteSpace': 'normal'},
        style_header={"fontWeight": "bold", "backgroundColor": "#f8f9fa"},
        page_size=20,
    )
])
