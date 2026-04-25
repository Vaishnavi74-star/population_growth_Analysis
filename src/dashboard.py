import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data_loader import WorldBankLoader
from .preprocess import preprocess_population_data
from .analysis import PopulationAnalyzer

# Initialize App with a premium theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

# Data Initial Load
loader = WorldBankLoader(cache_dir="data")
# Default countries for initial view
DEFAULT_COUNTRIES = ["WLD", "CHN", "IND", "USA", "IDN", "BRA", "NGA"]
raw_df = loader.fetch_all_indicators(DEFAULT_COUNTRIES)
df = preprocess_population_data(raw_df)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Population Growth Analytics Hub", className="text-center text-primary mb-4"), width=12)
    ], className="mt-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Controls"),
                dbc.CardBody([
                    html.Label("Select Countries:"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': c, 'value': c} for c in sorted(df['country'].unique())],
                        value=["World", "China", "India", "United States"],
                        multi=True,
                        className="mb-3"
                    ),
                    html.Label("Year Range:"),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=[df['year'].min(), df['year'].max()],
                        marks={str(y): str(y) for y in range(df['year'].min(), df['year'].max()+1, 10)},
                        step=1
                    )
                ])
            ], className="mb-4")
        ], width=12)
    ]),

    dbc.Tabs([
        dbc.Tab(label="Trends", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='line-chart'), width=12),
                dbc.Col(dcc.Graph(id='area-chart'), width=12)
            ], className="mt-3")
        ]),
        dbc.Tab(label="Regional Comparison", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-chart'), width=6),
                dbc.Col(dcc.Graph(id='pie-chart'), width=6)
            ], className="mt-3"),
            dbc.Row([
                dbc.Col(dcc.Graph(id='map-chart'), width=12)
            ])
        ]),
        dbc.Tab(label="Demographics (Rates)", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id='death-rate-chart'), width=6),
                dbc.Col(dcc.Graph(id='migration-chart'), width=6)
            ], className="mt-3")
        ]),
        dbc.Tab(label="Forecast", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Predict For:"),
                    dcc.Dropdown(id='forecast-country', value="India", className="mb-3"),
                    dcc.Graph(id='forecast-chart')
                ], width=12)
            ], className="mt-3")
        ])
    ])
], fluid=True)

@app.callback(
    [Output('line-chart', 'figure'),
     Output('area-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('map-chart', 'figure'),
     Output('death-rate-chart', 'figure'),
     Output('migration-chart', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_main_charts(selected_countries, year_range):
    filtered_df = df[
        (df['country'].isin(selected_countries)) & 
        (df['year'] >= year_range[0]) & 
        (df['year'] <= year_range[1])
    ]
    
    # 1. Line Chart (Population)
    line_fig = px.line(filtered_df, x='year', y='population', color='country', 
                       title="Population Growth Over Time", template="plotly_white")
    
    # 2. Area Chart (Cumulative Population)
    area_fig = px.area(filtered_df, x='year', y='population', color='country',
                       title="Cumulative Population Trends", template="plotly_white")
    
    latest_year = year_range[1]
    latest_df = df[df['year'] == latest_year]
    selected_latest_df = filtered_df[filtered_df['year'] == latest_year]
    
    # 3. Bar Chart (Top 10 in selected year)
    bar_df = latest_df.nlargest(10, 'population')
    bar_fig = px.bar(bar_df, x='population', y='country', orientation='h',
                     title=f"Top 10 Global Populations in {latest_year}", template="plotly_white")
    
    # 4. Pie Chart (Share of Selected Countries)
    pie_fig = px.pie(selected_latest_df, values='population', names='country',
                     title=f"Population Distribution in {latest_year}", hole=0.4)
    
    # 5. Map
    map_fig = px.choropleth(latest_df, locations="iso_code", color="population",
                             hover_name="country", title=f"Global Population Density ({latest_year})",
                             color_continuous_scale="Viridis")
    
    # 6. Death Rate Chart
    death_fig = px.line(filtered_df, x='year', y='death_rate', color='country',
                        title="Crude Death Rate (per 1,000 people)", template="plotly_white")
    
    # 7. Migration Chart
    migration_fig = px.line(filtered_df, x='year', y='net_migration', color='country',
                            title="Net Migration over Time", template="plotly_white")
    
    return line_fig, area_fig, bar_fig, pie_fig, map_fig, death_fig, migration_fig

@app.callback(
    [Output('forecast-country', 'options'),
     Output('forecast-chart', 'figure')],
    [Input('forecast-country', 'value'),
     Input('country-dropdown', 'value')]
)
def update_forecast(target_country, selected_countries):
    options = [{'label': c, 'value': c} for c in selected_countries]
    
    analyzer = PopulationAnalyzer(df)
    preds = analyzer.predict_future(target_country, horizon_years=50)
    
    if preds is None:
        return options, go.Figure()
        
    actual = df[df['country'] == target_country]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual['year'], y=actual['population'], name='Historical'))
    if 'exp_prediction' in preds:
        fig.add_trace(go.Scatter(x=preds['year'], y=preds['exp_prediction'], name='Exponential Forecast', line=dict(dash='dash')))
    if 'log_prediction' in preds:
        fig.add_trace(go.Scatter(x=preds['year'], y=preds['log_prediction'], name='Logistic Forecast', line=dict(dash='dot')))
        
    fig.update_layout(title=f"Population Forecast for {target_country} to 2070+", template="plotly_white")
    return options, fig

if __name__ == '__main__':
    app.run(debug=True, port=8051)
