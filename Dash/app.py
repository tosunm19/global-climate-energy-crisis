import dash
from dash import html, dcc

# Initialize Dash app with multi-page support
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server  # for deployment

# Main layout with navigation
app.layout = html.Div([

    html.Div([  # <-- MAIN CONTENT WRAPPER
        html.H1(
            "Global Climate & Energy Dashboard",
            style={
                'textAlign': 'left',
                'fontFamily': 'Segoe UI, sans-serif',
                'fontWeight': 'bold',
                'marginLeft': '20px'
            }
        ),

        html.Div([
            dcc.Link("Overview", href="/overview", style={
                'margin-right': '20px',
                'fontFamily': 'Segoe UI, sans-serif',
                'fontWeight': 'bold'
            }),

            dcc.Link("CO₂ Forecast", href="/forecast", style={
                'margin-right': '20px',
                'fontFamily': 'Segoe UI, sans-serif',
                'fontWeight': 'bold'
            }),

            dcc.Link("Energy Clusters", href="/emissions_energy", style={
                'fontFamily': 'Segoe UI, sans-serif',
                'fontWeight': 'bold'
            })
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),

        # <-- Page container that fills remaining viewport height
        dash.page_container
    ],
    style={
        "width": "75%",            # stay inside grey section
        "paddingRight": "40px",
        "boxSizing": "border-box",
        "height": "100vh",         # fill full viewport height
        "display": "flex",
        "flexDirection": "column"  # stack children vertically
    })

], style={
    'minHeight': '100vh',
    'padding': '20px',
    'display': 'flex',
    'flexDirection': 'column'
})

if __name__ == "__main__":
    app.run(debug=True)