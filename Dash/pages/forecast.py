import pandas as pd
from prophet import Prophet
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Register page (no need to import app)
dash.register_page(__name__, path="/forecast", name="CO₂ Forecast")

# Load dataset
df = pd.read_csv("data/processed/global_panel.csv")

# Page layout
layout = html.Div([

    html.H2("CO₂ Emissions Forecast",
            style={'textAlign': 'left',
                   'fontFamily': 'Segoe UI, sans-serif',
                   'fontWeight': 'bold',
                   }
            ),

    html.Label("Select Country:",
               style={'textAlign': 'left',
                      'fontFamily': 'Segoe UI, sans-serif',
                      'fontWeight': 'bold',
                      }),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in df['country'].unique()],
        value='United States',
        style={'textAlign': 'left',
               'fontFamily': 'Segoe UI, sans-serif',
               }
    ),

    html.Label("Forecast Horizon (Years):",
               style={'textAlign': 'left',
                      'fontFamily': 'Segoe UI, sans-serif',
                      }),

    dcc.Slider(
        id='forecast-slider',
        min=1, max=30, step=1, value=10,
        marks={i: str(i) for i in range(1, 31, 5)},
    ),

    # Only one Graph, placeholder for the callback
    dcc.Graph(
        id='forecast-graph',
        style={
            'border-radius': '7px',  # rounded corners
            'overflow': 'hidden',     # ensures plot is clipped inside corners
            'background-color': '#1a1a1a'
        }
    )

])


# Callback to update forecast
@dash.callback(
    Output('forecast-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('forecast-slider', 'value')
)
def update_forecast(selected_country, forecast_years):
    df_c = df[df['country'] == selected_country][['year', 'co2']].dropna()
    if df_c.empty:
        return {
            'data': [],
            'layout': {'title': f"No data for {selected_country}"}
        }

    df_c = df_c.rename(columns={'year': 'ds', 'co2': 'y'})
    df_c['ds'] = pd.to_datetime(df_c['ds'], format='%Y')

    m = Prophet(yearly_seasonality=False)
    m.fit(df_c)

    future = m.make_future_dataframe(periods=forecast_years, freq='YE')
    forecast = m.predict(future)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_c['ds'], y=df_c['y'], mode='markers+lines', name='Actual'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound',
                             hoverlabel=dict(font = dict(color ='white')),
                             line=dict(dash='dash', color='lightgrey')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound',
                             hoverlabel=dict(font = dict(color ='white')),
                             line=dict(dash='dash', color='lightgrey'),
                             fill='tonexty', fillcolor='rgba(200,200,200,0.2)'))

    fig.update_layout(
        title=f"CO₂ Emissions Forecast for {selected_country}",
        xaxis_title="Year",
        yaxis_title="CO₂ (million tons)",
        paper_bgcolor='#1a1a1a',  # figure background
        plot_bgcolor='#1a1a1a',  # plot area background
        font=dict(family='Segoe UI', color='white'),  # axis, title, legend font
        xaxis=dict(tickfont=dict(color='white'), title_font=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white'), title_font=dict(color='white')),
        legend=dict(
            orientation='h',
            x=0.5,
            y=-0.2,
            xanchor='center',
            yanchor='top',
            bgcolor= 'rgba(26,26,26,0.001)',  # semi-transparent black works reliably
            bordercolor='rgba(26,26,26,0.001)',
            borderwidth=1,
            font=dict(color='white')
        )
    )

    return fig
