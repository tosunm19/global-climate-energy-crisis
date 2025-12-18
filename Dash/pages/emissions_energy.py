import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
from dash import html, dcc
import dash
from dash.dependencies import Input, Output

# Register page
dash.register_page(__name__, path="/emissions_energy", name="Energy Clusters")

# Load dataset
df = pd.read_csv("data/processed/global_panel.csv")

# Available years
available_years = sorted(df['year'].unique(), reverse=True)

# Layout with year dropdown
layout = html.Div([
    html.H2("Country Clusters by CO₂ & Energy Profile",
        style={'textAlign': 'left',
               'fontFamily': 'Segoe UI, sans-serif',
               'fontWeight': 'bold',
               }
            ),

    html.Label("Select Year:",
               style={'textAlign': 'left',
               'fontFamily': 'Segoe UI, sans-serif',
               }
               ),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(y), 'value': y} for y in available_years],
        value=available_years[0],  # default = latest year
        clearable=False,
        style={'textAlign': 'left',
               'fontFamily': 'Segoe UI, sans-serif',
               }
    ),

    dcc.Graph(id='cluster-graph')
])


# Callback to update clustering plot
@dash.callback(
    Output('cluster-graph', 'figure'),
    Input('year-dropdown', 'value')
)
def update_clusters(selected_year):
    df_latest = df[df['year'] == selected_year]

    cluster_vars = [
        'co2_per_capita',
        'renewables_share_energy',
        'fossil_share_energy',
        'low_carbon_share_energy',
        'gdp'
    ]

    df_cluster = df_latest[['country'] + cluster_vars].dropna()

    if df_cluster.empty:
        return {
            'data': [],
            'layout': {'title': f"No complete data available for clustering in {selected_year}"}
        }

    # Standardize and cluster
    X_scaled = StandardScaler().fit_transform(df_cluster[cluster_vars])
    kmeans = KMeans(n_clusters=3, random_state=42).fit(X_scaled)
    df_cluster['cluster'] = kmeans.labels_

    # Dynamically assign cluster labels based on characteristics
    cluster_summary = df_cluster.groupby('cluster')[['co2_per_capita', 'renewables_share_energy']].mean()

    def assign_label_country(row, co2_median, renew_median):
        if row['co2_per_capita'] > co2_median and row['renewables_share_energy'] < renew_median:
            return "High CO₂, Fossil-heavy"
        elif row['co2_per_capita'] < co2_median and row['renewables_share_energy'] > renew_median:
            return "Low CO₂, Renewable-heavy"
        elif row['co2_per_capita'] < co2_median:
            return "Moderate CO₂, Balanced Energy"


    co2_median = df_cluster['co2_per_capita'].mean()
    renew_median = df_cluster['renewables_share_energy'].mean()

    df_cluster['cluster_label'] = df_cluster.apply(assign_label_country, axis=1, args=(co2_median, renew_median))

    # Scatter plot
    fig = px.scatter(
        df_cluster.reset_index(),
        x='co2_per_capita',
        y='renewables_share_energy',
        size='fossil_share_energy',
        color='cluster_label',
        hover_name='country',
        hover_data={col: True for col in cluster_vars},
        title=f"Country Clusters by CO₂ & Energy Profile ({selected_year})",
        size_max=60
    )
    fig.update_layout(xaxis_title="CO₂ per Capita", yaxis_title="Renewables Share (%)")

    return fig
