import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from dash import html, dcc
import dash
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/overview", name="Overview")

df = pd.read_csv("data/processed/global_panel.csv")
df_countries = df[~df["country"].str.contains("-", regex=False)]


# Global CO2 Emissions over time ----------------------------------------------------------------------------------
global_co2 = df.groupby("year")["co2"].sum().reset_index()

fig_global = px.line(
    global_co2,
    x="year",
    y="co2",
    title="Global CO₂ Emissions Over Time",
)

fig_global.update_layout(
    paper_bgcolor="#171717",
    plot_bgcolor="#171717",
    font=dict(color="white", family="Segoe UI"),
)


# Top 10 Emitters ----------------------------------------------------------------------------------
latest_year = df['year'][df['gdp'].notna()].max()

top_emitters = (
    df_countries[df_countries["year"] == latest_year]
    .sort_values(['co2'], ascending=False)
    .head(10)
    .sort_values(['co2'], ascending=True)
)

fig_top_emitters = px.bar(
    top_emitters,
    x="co2",
    y="country",
    orientation='h',
    title=f"Top 10 CO₂ Emitters in {latest_year}",
)

fig_top_emitters.update_layout(
    paper_bgcolor="#171717",
    plot_bgcolor="#171717",
    font=dict(color="white", family="Segoe UI"),
    margin=dict(l=40, r=40, t=60, b=40),
)



# Top 10 GDP ----------------------------------------------------------------------------------
top_gdp = (
    df_countries[df_countries["year"] == latest_year]
    .sort_values(['gdp'], ascending=False)
    .head(10)
    .sort_values(['gdp'], ascending=True)
)

fig_top_gdp = px.bar(
    top_gdp,
    x="gdp",
    y="country",
    orientation='h',
    title=f"Top 10 GDP in {latest_year}",
)
# fig_top_emitters.update_yaxes(autorange="reversed")

fig_top_gdp.update_layout(
    paper_bgcolor="#171717",
    plot_bgcolor="#171717",
    font=dict(color="white", family="Segoe UI"),
    margin=dict(l=40, r=40, t=60, b=40),
)



# ------ LAYOUT -------

layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",
        "padding": "20px",
        "boxSizing": "border-box",
        "width": "100%",
        "minWidth": "0",
    },
    children=[
        html.H2(
            "Overview",
            style={
                'textAlign': 'left',
                'fontFamily': 'Segoe UI, sans-serif',
                'fontWeight': 'bold',
                'color': 'white'
            }
        ),

        # Global CO2 plot (top 40% of screen)
        dcc.Graph(
            id="global-co2-graph",
            figure=fig_global,
            style={
                'width': '100%',
                'height': '40vh',  # <-- scale to 40% of viewport
                'border-radius': '7px',
                'overflow': 'hidden',
                'background-color': '#171717',
                'margin-bottom': '20px'
            }
        ),

        # Bottom two plots (take 60% of screen height)
        html.Div(
            children=[
                html.Div(
                    style={"flex": "1", "padding": "10px"},
                    children=[dcc.Graph(
                        id="top-emitters-graph",
                        figure=fig_top_emitters,
                        style={
                            'width': '100%',
                            'height': '100%',  # <-- fill parent container
                            'border-radius': '7px',
                            'overflow': 'hidden',
                            'background-color': '#171717'
                        }
                    )]
                ),
                html.Div(
                    style={"flex": "1", "padding": "10px"},
                    children=[dcc.Graph(
                        id="top-gdp-graph",
                        figure=fig_top_gdp,
                        style={
                            'width': '100%',
                            'height': '100%',
                            'border-radius': '7px',
                            'overflow': 'hidden',
                            'background-color': '#171717'
                        }
                    )]
                ),
            ],
            style={
                "display": "flex",
                "flex": "1",          # <-- takes remaining 60% of container height
                "flexDirection": "row"
            }
        )
    ]
)





